from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')



@bp.route('/hello')
def hello_flex():
    return 'flexxxx'

#<전처리 완료 페이지 모음, 여기 써있는 페이지들은 작업 가능. 이 함수들은 추후 삭제 -----
@bp.route('/client_init')
def init():
    return render_template('client_templates/homepage-1.html')

@bp.route('/client_404')
def init404():
    return render_template('client_templates/404-1.html')

@bp.route('/client_article')
def article():
    return render_template('client_templates/article-sidebar-right.html')

@bp.route('/client_contact')
def contact():
    return render_template('client_templates/contact-us.html')


@bp.route('/client_gallery')
def gallery():
    return render_template('client_templates/gallery.html')


@bp.route('/client_movieInfo')
def movieInfo():
    return render_template('client_templates/movie-info-sidebar-right.html')


@bp.route('/client_moviesList')
def movieList():
    return render_template('client_templates/movies-list.html')


@bp.route('/client_news')
def newsBlock():
    return render_template('client_templates/news-blocks-sidebar-right.html')


@bp.route('/client_underConstruction')
def underConstruction():
    return render_template('client_templates/under-construction.html')
#----->


@bp.route('/')
def index():
    return render_template('client_templates/homepage-1.html')


@bp.route('/ques')
def index2():
    return redirect(url_for('question._list'))
