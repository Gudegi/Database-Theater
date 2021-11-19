from flask import Flask, render_template, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from flask_admin import Admin
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import helpers as admin_helpers

import config

db = SQLAlchemy()
migrate = Migrate()


# Create admin
admin = Admin(name='My Dashboard', base_template='admin_base.html', template_mode='bootstrap4')
from .models import Screen, User, Role, Movie, Screenschedule, Question, Answer
# Add model views
from .views.admin_views import MyModelView, ScheduleView, UserView, CustomView, MovieView, QuestionView, AnswerView
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(MovieView(Movie, db.session, menu_icon_type='fa', menu_icon_value='fa-film', name="Movies", endpoint='moives'))
admin.add_view(ScheduleView(Screenschedule,  db.session, menu_icon_type='fa', menu_icon_value='fa-calendar-check-o', name='Screen Schedule'))

admin.add_view(QuestionView(Question,  db.session, menu_icon_type='fa', menu_icon_value='fa-calendar-check-o', name='Question', endpoint='questions'))
admin.add_view(AnswerView(Answer,  db.session, menu_icon_type='fa', menu_icon_value='fa-calendar-check-o', name='Answer', endpoint='answers'))

# endpoint는 URI 마지막 의미(/admin/custom)
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
    from .views import main_views, question_views, answer_views, movies_views, auth_views, reservation_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(movies_views.bp)
    app.register_blueprint(reservation_views.bp)
    
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

    #  오류 처리
    app.register_error_handler(404, page_not_found)
    return app

