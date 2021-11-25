from flask import Blueprint, url_for, render_template, g, request, flash
from werkzeug.utils import redirect

from datetime import datetime

from ..views.auth_views import login_required

from flex import db
from flex.forms import ReviewForm
from flex.models import Movie, Actor, Review

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
    review_list = Review.query.filter(Review.movie_id == movie_id).all()
    return render_template('client_templates/movie-info-sidebar-right.html', movie=movie, actor_list=actor_list, review_list=review_list)


@bp.route('/detail/<int:movie_id>/create', methods=('GET', 'POST'))
@login_required
def create_review(movie_id):
    form = ReviewForm()
    if request.method == 'POST' and form.validate_on_submit():
        movie = Movie.query.get_or_404(movie_id)
        review = Review(title=form.title.data,
                        content=form.content.data,
                        date=datetime.now(),
                        rate=form.rate.data,
                        movie_id=movie.id,
                        member_id=g.member.id)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movies.detail', movie_id=movie.id))
    return render_template('client_templates/review_comment.html', form=form)


@bp.route('/detail/<int:movie_id>/<int:review_id>', methods=('GET', 'POST'))
@login_required
def modify_review(movie_id, review_id):
    review_ = Review.query.get(review_id)
    if g.member.id != review_.member_id:
        flash('수정권한이 없습니다.')
        return redirect(url_for('movies.detail', movie_id=movie_id))
    if request.method == 'POST':
        form = ReviewForm()
        if form.validate_on_submit():
            form.populate_obj(review_)
            review_.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('movies.detail', movie_id=movie_id))
    else:
        form = ReviewForm(obj=review_)
    return render_template('client_templates/review_comment.html', form=form)


@bp.route('/detail/<int:movie_id>/delete<int:review_id>')
@login_required
def delete_review(movie_id, review_id):
    review_ = Review.query.get(review_id)
    if g.member.id != review_.member_id:
        flash('삭제권한이 없습니다.')
        return redirect(url_for('movies.detail', movie_id=movie_id))
    db.session.delete(review_)
    db.session.commit()
    return redirect(url_for('movies.detail', movie_id=movie_id))