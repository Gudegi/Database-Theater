from flask import Flask, url_for, redirect, render_template, request, abort
from flask_admin.base import AdminIndexView
from flask_security import current_user
from flask_admin import BaseView, expose    
from flask_admin.contrib.sqla import ModelView
import json, base64

from wtforms import PasswordField


from ..models import Facility, User, Member, Evaluation, Theater, Seat
 
from .. import db
#홈 화면 커스텀
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        #movie_list = Movie.query.order_by(Movie.id.desc())
        user_count = User.query.count()
        
        #지난 30일 간 매출
        prev_month_pay_query = db.text("SELECT SUM(firstpay) FROM pay NATURAL JOIN reservation \
            WHERE pay.reservation_id = reservation.id and reservation.date between DATE_ADD(CURDATE(), INTERVAL -30 DAY) and CURDATE()")
        p_result = db.session.execute(prev_month_pay_query)
        prev_month_pay = int(p_result.fetchone()[0])
        if len(str(prev_month_pay)) <= 6:
            prev_month_pay = str(prev_month_pay)
            prev_month_pay = prev_month_pay[:3] +','+ prev_month_pay[3:]

        #사용자 수
        client_count = Member.query.count()

        #최고 히트작(좌석 제일 많이 팔린 영화)
        movie_sales_query = db.text("SELECT title, SUM(firstpay) as total FROM movie, \
            (SELECT movie_id, firstpay FROM screenschedule, \
                (SELECT pay.firstpay, screen_schedule_id FROM pay, reservation WHERE pay.reservation_id = reservation.id) AS A  WHERE screenschedule.id = A.screen_schedule_id) AS B \
                    WHERE movie.id = B.movie_id GROUP BY title ORDER BY total DESC;")
        best_seller_result = db.session.execute(movie_sales_query)
        best_movie = best_seller_result.fetchone()

        
        #movie_sales_data= {'movies': [ {'title': '싱크홀', 'sales': 337000}, {'title': '신과함께-인과 연', 'sales': 7000 } ] }
        #영화 판매 파이차트
        movie_sales_result = db.session.execute(movie_sales_query)
        movie_sales = movie_sales_result.fetchall()
        movie_sales_data = { "movies": [ ] }
        for title, sales in movie_sales:
            movie_sales_data["movies"].append( {"title":title, "sales":int(sales)})
    
        #연봉 히스토그램
        salary_query = db.text("SELECT salary, COUNT(salary) FROM user GROUP BY salary")
        salary_result = db.session.execute(salary_query)
        salary = salary_result.fetchall()
        salary_data = { "salary": [ ] }
        for money, count in salary:
            salary_data["salary"].append( {"salary":money, "count":count})
    

        return self.render('admin/index.html',  user_count=user_count, prev_month_pay=prev_month_pay, client_count=client_count, \
            best_movie=best_movie, movie_sales_data= movie_sales_data, salary_data=salary_data)


# Create customized model view class
class MyModelView(ModelView):
    #active 상태가 아니거나, 권한 없으면 false
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('일반') or current_user.has_role('시설물관리') or current_user.has_role('스케줄관리') or current_user.has_role('인사관리') or current_user.has_role('근태관리') or current_user.has_role('관리자'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
    
    
    #can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

    column_hide_backrefs = False
    column_display_pk = True
 
class UserView(MyModelView):
    
    edit_modal = False
    create_modal = False
    can_export = False
    can_view_details = False
    can_create= False
    can_delete = False
    can_edit = False
    #details_modal = False
    

    #column_descriptions = dict(roles='권한')
    column_list= [ 'userTheater', 'userName', 'department_info',  'gender', 'email', 'birth_date', 'phone', 'salary' ]
    column_searchable_list = [ 'department_info',  'gender', 'email', 'birth_date', 'phone', 'salary' ]
    column_labels = dict( userTheater='지점', userName='이름', department_info='직책', gender='성별', email='이메일', birth_date='생년월일', phone='전화번호', salary='연봉(만원)')
    column_choices = {
            'gender': [('male', '남성'), ('female', '여성')]
        }
    
    def get_query(self):
        #관리자, 인사관리는 모든 직원의  모든  정보를  볼  수  있다.
        if current_user.has_role('인사관리') or current_user.has_role('관리자'):
            return self.session.query(User.id, 
            Theater.name.label('userTheater'), 
            (User.last_name + User.first_name).label('userName'),
            User.department_info.label('department_info'),
            User.gender,
            User.email,
            User.birth_date,
            User.phone,
            User.salary
            ).filter(User.theater_id == Theater.id).order_by(Theater.name).order_by((User.last_name + User.first_name).label('userName'))
        #그 외 사람들은 일반적인 정보만 볼 수 있다.
        else:
            return self.session.query(User.id, 
            Theater.name.label('userTheater'), 
            (User.last_name + User.first_name).label('userName'),
            User.department_info.label('department_info'),
            User.gender,
            User.email,
            ).filter(User.theater_id == Theater.id).order_by(Theater.name).order_by((User.last_name + User.first_name).label('userName'))

#영화 목록
class MovieView(MyModelView):
    column_editable_list = ['title', 'genre', 'age', 'director', 'eng_title']
    column_searchable_list = ['title', 'genre', 'age', 'director', 'eng_title']
    column_filters = ['title', 'genre', 'age', 'director', 'eng_title']
    column_labels = dict(title='타이틀', eng_title='타이틀(영어)', genre='장르', age='연령 제한', running_time='러닝 타임', information='줄거리' \
        , director='감독', release='개봉일', country='제작국가', language='언어' )

#영화 상영 일정 관리
class ScheduleView(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('스케줄관리') or current_user.has_role('관리자'):
            return True

        return False
    column_list = ('session','screen', 'title', 'theater', 'starttime','endtime') #역참조를 이용하여 영화 title 가져옴(이렇게 하면 여기서 추가 가능)
    column_labels = dict(session='회차', screen_number='상영관(ID)', screen='상영관', movie_id = '영화(ID)', title='타이틀', \
        theater_id = '극장(ID)', theater='지점', starttime='시작시간', endtime='종료시간')
    column_searchable_list = ['session','screen_number', 'movie_id', 'theater_id', 'starttime','endtime']
    column_filters = ['session','screen_number', 'movie_id', 'theater_id', 'starttime','endtime']
   
#출근
class CommuteView(MyModelView):
    column_list = [ 'user', 'type', 'date', 'starttime', 'endtime', 'work_time']
    column_labels = dict(user='이름', type='근무형태', date='날짜', starttime='시작시간', endtime='마감시간', work_time='작업시간'  )
    #column_editable_list = column_list
    #column_searchable_list = column_editable_list


#시설 관리
class FacilityView(MyModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('시설물관리') or current_user.has_role('관리자'):
            return True

        return False

    def get_query(self):
        return super(FacilityView, self).get_query().filter(Facility.theater_id == current_user.theater_id )
    
    column_list = ['id', 'name', 'place', 'installdate', 'inspectiondate']
    column_labels= dict(id='시설ID', name='시설이름', place='위치', installdate='설치일자', inspectiondate='점검일자')

#직원 관리
class ManageUserView(MyModelView):
    
    column_list = [ 'email', 'first_name', 'last_name' , 'roles', 'role_name', 'theater_id']
    
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('근태관리') or current_user.has_role('관리자'):
            return True

        return False
   
    def get_query(self):
        return super(ManageUserView, self).get_query().filter(User.theater_id == current_user.theater_id )
    

#인사 평가
class EvaluationView(MyModelView):

    column_list = ('userTheater', 'userName', 'department_info', 'score', 'comment', 'date'  )
    column_labels = dict(userTheater='지점', userName='이름', department_info='직책', score='평가(1~5)', comment='평가내용', date='작성일자')
     
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('인사관리') or current_user.has_role('관리자'):
            return True

        return False

    def get_query(self):
        #인사관리 권한을 가진 부점장, 점장은 지점 직원들을 평가 할 수 있다.

        if current_user.has_role('인사관리'):
            return self.session.query(Evaluation.id, 
            Theater.name.label('userTheater'), 
            (User.last_name + User.first_name).label('userName'),
            User.department_info.label('department_info'),
            Evaluation.score,
            Evaluation.comment, 
            Evaluation.date).filter(User.theater_id == Theater.id).\
                filter(Evaluation.user_id == User.id).\
                filter(User.theater_id == current_user.theater_id)
        
        #관리자는 모든 직원을 평가할 수 있다.
        else:
            return self.session.query(Evaluation.id, 
            (User.last_name + User.first_name).label('userName'),
            User.department_info.label('department_info'),
            Theater.name.label('userTheater'), 
            Evaluation.score,
            Evaluation.comment, 
            Evaluation.date).filter(User.theater_id == Theater.id).\
                filter(Evaluation.user_id == User.id)  

class NoticeView(MyModelView):
    column_list = ('id', 'theater', 'title', 'content', 'date')
    column_labels = dict(id='공지 번호', theater='지점', title='제목', content='내용',  date='작성일자')

class InquiryView(MyModelView):
    column_list = ('number', 'title', 'content', 'member_id', 'date')
    column_labels = dict(number='문의 번호', title='문의 제목', content='내용',  membdate='작성일자')

class QuestionView(MyModelView):
    column_hide_backrefs = False
    column_editable_list = ['subject', 'content', 'create_date']
    column_searchable_list = column_editable_list

class AnswerView(MyModelView):
    column_hide_backrefs = False
    column_list = ('questionSubject', 'questionContent', 'content', 'create_date')
    column_editable_list = ['id', 'question_id',  'content', 'create_date']
    #question
    column_searchable_list = column_editable_list


class TestView(MyModelView):

    def get_query(self):
        return super(TestView, self).get_query().filter(User.theater_id== current_user.theater_id)

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')

