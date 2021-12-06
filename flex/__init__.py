from flask import Flask, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers

import config

db = SQLAlchemy()
migrate = Migrate(compare_type=True)


# Create admin
from .views.admin_views import MyHomeView, CommuteView, ManageUserView, MyModelView, NoticeView, ScheduleView, UserView, CustomView, MovieView, QuestionView, AnswerView, FacilityView, TestView, EvaluationView
admin = Admin(index_view=MyHomeView(), name='DMN Manage', base_template='admin_base.html', template_mode='bootstrap4')
from .models import Evaluation, Facility, User, Role, Movie, Screenschedule, Question, Answer, Commute, Notice
# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name='전체 직원 조회', endpoint='users'))
admin.add_view(MovieView(Movie, db.session, menu_icon_type='fa', menu_icon_value='fa-film', name='영화 목록', endpoint='moives'))
admin.add_view(ScheduleView(Screenschedule,  db.session, menu_icon_type='fa', menu_icon_value='fa-calendar-check-o', name='상영 일정 관리', endpoint='screenschedules'))
admin.add_view(CommuteView(Commute, db.session, menu_icon_type='fa', menu_icon_value='fa-clock-o', name='출근부', endpoint='commute' ))
admin.add_view(FacilityView(Facility, db.session, menu_icon_type='fa', menu_icon_value='fa-wrench', name='시설물 조회', endpoint='facilitys'))
admin.add_view(ManageUserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-user-plus', name='내 지점 직원 관리', endpoint='manageUsers' ))
admin.add_view(EvaluationView(Evaluation, db.session, menu_icon_type='fa', menu_icon_value='fa-pencil-square-o', name='내 지점 인사 평가', endpoint='evaluation' ))
admin.add_view(NoticeView(Notice, db.session, menu_icon_type='fa', menu_icon_value='fa-exclamation', name='지점 별 공지', endpoint='notice'  ))

admin.add_view(TestView(User,db.session,endpoint='asdf', name='test'))
admin.add_view(QuestionView(Question,  db.session, menu_icon_type='fa', menu_icon_value='fa-calendar-check-o', name='Question', endpoint='questions',category="model"))
admin.add_view(AnswerView(Answer,  db.session, menu_icon_type='fa', menu_icon_value='fa-calendar-check-o', name='Answer', endpoint='answers',category="model"))

admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))


# Form Extentions
from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired
class ExtendedRegisterForm(RegisterForm):
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])


def page_not_found(e):
    return render_template('client_templates/404-1.html'), 404


def create_app():
    app = Flask(__name__)
    #app.config 환경 변수를 부름
    app.config.from_object(config)
    #flask admin 초기화
    admin.init_app(app)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)


    # 블루프린트
    from .views import main_views, question_views, answer_views, movies_views, auth_views, reservation_views, mypage_views, theaters_views, chat_views,services_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(movies_views.bp)
    app.register_blueprint(reservation_views.bp)
    app.register_blueprint(mypage_views.bp)
    app.register_blueprint(theaters_views.bp)
    app.register_blueprint(services_views.bp)
    app.register_blueprint(chat_views.bp)


    # 직원
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form = ExtendedRegisterForm)
    
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
    )

    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    #  오류 처리
    app.register_error_handler(404, page_not_found)
    return app

