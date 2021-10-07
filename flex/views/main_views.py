from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_flex():
    return 'flexxxx'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))