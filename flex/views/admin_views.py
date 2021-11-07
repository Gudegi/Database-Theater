
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_admin import BaseView, expose    
from flask_admin.contrib import sqla
from wtforms import PasswordField



# Create customized model view class
class MyModelView(sqla.ModelView):
    #active 상태가 아니거나, 권한 없으면 false
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        #superuser가 아니면 안보이는 페이지
        if current_user.has_role('최고관리자') or current_user.has_role('상영스케쥴관리자'):
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

class UserView(MyModelView):
    column_hide_backrefs = False
    column_display_pk = True
    column_list = ('email', 'first_name', 'last_name', 'roles')

    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    #form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_overrides = {
        'password': PasswordField
    }

#영화 목록
class MovieView(MyModelView):
    #column_editable_list = ['title', 'genre', 'age', 'director', 'eng_title']
    column_searchable_list = ['title', 'genre', 'age', 'director', 'eng_title']
    column_filters = ['title', 'genre', 'age', 'director', 'eng_title']

#영화 스케쥴 관리
class ScheduleView(MyModelView):
    column_display_pk = True # pk 보이기
    #column_hide_backrefs = False # fk 보이기
    #column_list = ('session','screen_number', 'movie_id','title', 'theater_id', 'starttime','endtime') #이걸로 써야지 외래키도 보임
    column_list = ('session','screen_number', 'title', 'theater_id', 'starttime','endtime') #역참조를 이용하여 영화 title 가져옴(이렇게 하면 여기서 추가 가능)
    column_searchable_list = ['session','screen_number', 'movie_id', 'theater_id', 'starttime','endtime']
    column_filters = ['session','screen_number', 'movie_id', 'theater_id', 'starttime','endtime']
    


class QuestionView(MyModelView):
    column_hide_backrefs = False
    column_display_pk = True
    column_editable_list = ['subject', 'content', 'create_date']
    column_searchable_list = column_editable_list

class AnswerView(MyModelView):
    column_hide_backrefs = False
    column_display_pk = True
    column_list = ('question', 'content', 'create_date')
    column_editable_list = ['id', 'question_id',  'content', 'create_date']
    #question
    column_searchable_list = column_editable_list

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')