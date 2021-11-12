from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
'''
from flask_security import Security
from flask_admin import helpers as admin_helpers
from adminlte.admin import AdminLte, admins_store'''

import config

db = SQLAlchemy()
migrate = Migrate()


def page_not_found(e):
    return render_template('client_templates/404-1.html'), 404


def create_app():
    app = Flask(__name__)
    #app.config 환경 변수를 부름
    app.config.from_object(config)

    '''
    ###adminLte
    security = Security(app, admins_store)
    admin = AdminLte(app, skin = 'green', name = 'FlaskCMS', short_name = "<b>F</b>C", long_name = "<b>Flask</b>CMS")
    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template = admin.base_template,
            admin_view = admin.index_view,
            h = admin_helpers,
            #get_url = url_for
        )
    '''
    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, question_views, answer_views, movies_views, auth_views, theaters_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(movies_views.bp)
    app.register_blueprint(theaters_views.bp)

    
    #   오류 처리
    app.register_error_handler(404, page_not_found)
    return app

