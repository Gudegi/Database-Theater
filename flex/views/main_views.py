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

