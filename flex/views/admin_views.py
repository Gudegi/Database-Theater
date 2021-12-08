from flask import Flask, url_for, redirect, render_template, request, abort
from flask_admin.base import AdminIndexView
from flask_security import current_user
from flask_admin import BaseView, expose    
from flask_admin.contrib.sqla import ModelView

from ..models import Facility, User, Member, Evaluation, Theater, Notice
 
from .. import db
#홈 화면 커스텀
class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        #movie_list = Movie.query.order_by(Movie.id.desc())
        user_count = User.query.count()
        
        #지난 30일 간 매출, (판매액)
        prev_month_pay_query = db.text("SELECT SUM(firstpay) FROM pay NATURAL JOIN reservation \
            WHERE pay.reservation_id = reservation.id and reservation.date between DATE_ADD(CURDATE(), INTERVAL -30 DAY) and CURDATE()")
        p_result = db.session.execute(prev_month_pay_query)
        prev_month_pay = int(p_result.fetchone()[0])
        prev_month_pay = format(prev_month_pay, ",") #3자리 ,

        #사용자 수
        client_count = Member.query.count()
        client_count = format(client_count, ",")

        #최고 히트작(판매액 최대 영화), (영화, 판매액)
        movie_sales_query = db.text("SELECT title, SUM(firstpay) as total FROM movie, \
            (SELECT movie_id, firstpay FROM screenschedule, \
                (SELECT pay.firstpay, screen_schedule_id FROM pay, reservation WHERE pay.reservation_id = reservation.id) AS A  WHERE screenschedule.id = A.screen_schedule_id) AS B \
                    WHERE movie.id = B.movie_id GROUP BY title ORDER BY total DESC;")
        best_seller_result = db.session.execute(movie_sales_query)
        best_movie, best_movie_sales = best_seller_result.fetchone()
        best_movie_sales = format(best_movie_sales, ",")
        best = [best_movie, best_movie_sales]

        #movie_sales_data= {'movies': [ {'title': '싱크홀', 'sales': 337000}, {'title': '신과함께-인과 연', 'sales': 7000 } ....] }
        #영화 판매 파이차트
        movie_sales_result = db.session.execute(movie_sales_query)
        movie_sales = movie_sales_result.fetchall()
        movie_sales_data = { "movies": [ ] }
        for title, sales in movie_sales:
            movie_sales_data["movies"].append( {"title":title, "sales":int(sales)})
    
        #연봉 히스토그램, (연봉, 사람수)
        salary_query = db.text("SELECT salary, COUNT(salary) FROM user GROUP BY salary")
        salary_result = db.session.execute(salary_query)
        salary = salary_result.fetchall()
        salary_data = { "salary": [ ] }
        for money, count in salary:
            salary_data["salary"].append( {"salary":money, "count":count})
        #직급 분포, (직급, 사람수)
        position_query = db.text("SELECT department_info, COUNT(department_info) FROM user GROUP BY department_info")
        position_result = db.session.execute(position_query)
        position = position_result.fetchall()
        position_dict = {}
        for position_name, position_count in position:
            position_dict[position_name] = position_count
        position_dict['합계'] = sum(position_dict.values())

        #월별 영화 매출, (월, 영화, 판매액)
        movie_sales_month_query = db.text("SELECT MONTH(B.date), title, SUM(firstpay) FROM movie, \
            (SELECT movie_id, A.firstpay, A.date FROM screenschedule, \
                ((SELECT reservation.date, pay.firstpay, reservation.screen_schedule_id FROM pay, reservation WHERE pay.reservation_id = reservation.id) AS A) \
                     WHERE screenschedule.id = A.screen_schedule_id) AS B \
                         WHERE movie.id = B.movie_id GROUP BY title, MONTH(B.date) ORDER BY MONTH(B.date);")
        movie_sales_month_result = db.session.execute(movie_sales_month_query)
        movie_sales_month = movie_sales_month_result.fetchall()
        movie_sales_month_data = {"movies": [ ] }
        for month, title, sales in movie_sales_month:
            movie_sales_month_data["movies"].append( {"month":month, "title":title, "sales":int(sales)})

        #월별 지점 매출, (월, 지점, 판매액)
        theater_sales_month_query = db.text("SELECT MONTH(B.date), theater.name, SUM(B.firstpay) FROM theater, \
            ((SELECT A.firstpay, A.date, screenschedule.theater_id FROM screenschedule, \
                ((SELECT reservation.date, pay.firstpay, reservation.screen_schedule_id FROM pay, reservation WHERE pay.reservation_id = reservation.id) AS A) \
                    WHERE screenschedule.id = A.screen_schedule_id) AS B) \
                        WHERE theater.id = B.theater_id GROUP BY theater.name, MONTH(B.date) ORDER BY MONTH(B.date) asc;")
        theater_sales_month_result = db.session.execute(theater_sales_month_query)
        theater_sales_month = theater_sales_month_result.fetchall()
        theater_sales_month_data = {"movies": [ ] }
        for month, theater, sales in theater_sales_month:
            theater_sales_month_data["movies"].append( {"month":month, "theater":theater, "sales":int(sales)})

        #멤버십 분포 (랭크, 사람수)
        membership_query = db.text("SELECT rank, COUNT(rank) FROM membership GROUP BY rank")
        membership_result = db.session.execute(membership_query)
        membership = membership_result.fetchall()
        membership_data = { "membership": [ ] }
        for rank, count in membership:
            membership_data["membership"].append( {"rank":rank, "count":count})


        
        return self.render('admin/index.html',  user_count=user_count, prev_month_pay=prev_month_pay, client_count=client_count, \
            best_movie=best, movie_sales_data= movie_sales_data, salary_data=salary_data, position_dict=position_dict, \
            movie_sales_month_data=movie_sales_month_data, theater_sales_month_data=theater_sales_month_data, membership_data = membership_data)


# Create customized model view class
class MyModelView(ModelView):
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
#전체 직원 조회
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

    column_list = ('session','screen', 'title', 'theater', 'starttime','endtime') #역참조를 이용하여 영화 title 가져옴(이렇게 하면 여기서 추가 가능)
    column_labels = dict(session='회차', screen_number='상영관(ID)', screen='상영관', movie_id = '영화(ID)', title='타이틀', \
        theater_id = '극장(ID)', theater='지점', starttime='시작시간', endtime='종료시간')
    column_searchable_list = ['session','screen_number', 'movie_id', 'theater_id', 'starttime','endtime']
    column_filters = ['session','screen_number', 'movie_id', 'theater_id', 'starttime','endtime']

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('스케줄관리') or current_user.has_role('관리자'):
            return True

        return False
   
#출근부
class CommuteView(MyModelView):
    column_list = [ 'userTheater', 'user', 'type', 'date', 'starttime', 'endtime', 'work_time']
    column_labels = dict(userTheater='지점', user='이름', type='근무형태', date='날짜', starttime='시작시간', endtime='마감시간', work_time='작업시간'  )
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
        if current_user.has_role('관리자'):
            return super(FacilityView, self).get_query().filter()
        else:
            return super(FacilityView, self).get_query().filter(Facility.theater_id == current_user.theater_id )
    
    column_list = ['theater', 'id', 'name', 'place', 'installdate', 'inspectiondate']
    column_labels= dict(theater='지점', id='시설ID', name='시설이름', place='위치', installdate='설치일자', inspectiondate='점검일자')

#직원 관리
class ManageUserView(MyModelView):
    
    column_list = [ 'theater', 'email', 'first_name', 'last_name' , 'department_info', 'salary', 'roles', 'account', 'confirmed_at']
    column_labels = dict(theater='지점', last_name='성', first_name='이름', roles='권한', email='이메일', salary='연봉', department_info='직책', confirmed_at='입사일', account='계좌')

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('근태관리') or current_user.has_role('관리자'):
            return True

        return False
   
    def get_query(self):
        if current_user.has_role('관리자'):
            return super(ManageUserView, self).get_query().filter()
        else:
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

#공지 관리
class NoticeView(MyModelView):
    column_list = ('id', 'theater', 'title', 'content', 'date')
    column_labels = dict(id='공지 번호', theater='지점', title='제목', content='내용',  date='작성일자')

    def get_query(self):
        if current_user.has_role('관리자'):
            return super(NoticeView, self).get_query().filter()
        else:
            return super(NoticeView, self).get_query().filter(Notice.theater_id == current_user.theater_id )

#문의 확인
class InquiryView(MyModelView):
    column_list = ('number', 'title', 'content', 'member_id', 'date')
    column_labels = dict(number='문의번호', title='문의제목', content='내용', member_id='작성자', date='작성일자')

#문의 답변
class InquiryAnswerView(MyModelView):
    column_list = ('inquiry_id', 'inquiry', 'inquiryContent', 'inquiryMember', 'content', 'create_date')
    column_labels = dict(inquiry_id='문의번호', inquiry='문의제목', inquiryContent='내용', inquiryMember='작성자', content='답변', create_date='답변작성일자')


'''class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')'''

