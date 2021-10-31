from flask import Blueprint, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

from werkzeug.utils import redirect

from .. import db
from flex.models import User, Role


bp = Blueprint('employee', __name__, url_prefix='/employee')

'''

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(bp, user_datastore)

# Create a user to test with
@bp.before_first_request
def create_user():
    db.create_all()
    user_datastore.create_user(email='matt@nobien.net', password='password')
    db.session.commit()

# Views
@bp.route('/')
@login_required
def home():
    return render_template('index.html')'''