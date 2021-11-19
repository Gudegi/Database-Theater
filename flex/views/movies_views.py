from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
from flex.models import Movie, Actor

bp = Blueprint('movies', __name__, url_prefix='/movies')

#영화 목록 페이지
@bp.route('/')
def list():
    movie_list = Movie.query.order_by(Movie.id.desc())
    return render_template('client_templates/movies-list.html', movie_list = movie_list)

#영화 목록 페이지에서 영화 이름 누르면 해당 영화 detail 페이지 랜더링, 각 영화의 이미지, 이름 등 db에 있는 정보들을 인자로 넘겨서 랜더링

@bp.route('/detail/<int:movie_id>')
def detail(movie_id):
    movie = Movie.query.get(movie_id)
    actor_list = Actor.query.filter(Actor.movie_id == movie_id).all()
    return render_template('client_templates/movie-info-sidebar-right.html', movie = movie, actor_list = actor_list)