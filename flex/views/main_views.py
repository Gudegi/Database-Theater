from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
from flex.models import Movie, Review
import datetime

bp = Blueprint('main', __name__, url_prefix='/')



@bp.route('/hello')
def hello_flex():
    return 'flexxxx'

@bp.route('/')
def init():
    movie_list = Movie.query.order_by(Movie.id.desc())
    rate_list = []
    for movie in movie_list:
        this_list = []
        review_list = Review.query.filter(Review.movie_id == movie.id).all()
        sum = 0
        num = 0
        for review in review_list:
            sum += review.rate
            num += 1
        if (num > 0):
            rate = round(sum / num, 2)
        else:
            rate = 0
        this_list.append(movie)
        this_list.append(rate)
        rate_list.append(this_list)
    today = datetime.date.today().strftime('%Y/%m/%d')
    return render_template('client_templates/homepage-1.html', movie_list=rate_list, today=today)

@bp.route('/client_init')
def index():
    return render_template('client_templates/homepage-1.html')

#<전처리 완료 페이지 모음, 여기 써있는 페이지들은 작업 가능. 이 함수들은 추후 삭제 -----


'''
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


@bp.route('/ques')
def index2():
    return redirect(url_for('question._list'))
'''