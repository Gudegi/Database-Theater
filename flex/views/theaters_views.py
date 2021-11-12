from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from werkzeug.utils import redirect
from flex.models import Theater, Screenschedule, Movie
from sqlalchemy import and_

bp = Blueprint('theaters', __name__, url_prefix='/theaters')

@bp.route('/', methods=['GET'])
def index():
    theaters = Theater.query.get(1)
    week = {0:'월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
    week_list = []
    now = datetime.now()
    now_weekday = now.weekday()

    args = request.args
    selected_date = args.get('date', now.strftime('%Y-%m-%d'))
    selected_theater_id = theaters.id

    # 오늘부터 다음주까지의 요일을 표시
    for i in range(now_weekday, now_weekday+7):
        day = i - now_weekday
        date = now + timedelta(days=day)
        i %= 7
        week_list.append({'weekday' : week[i], 'date':date.strftime('%Y-%m-%d')})

    # 해당 극장에 해당하는 영화만 보여줌
    if selected_theater_id:
        movies = Movie.query.join(Screenschedule, and_(Screenschedule.movie_id == Movie.id, Screenschedule.theater_id == selected_theater_id))
    else:
        movies = Movie.query.join(Screenschedule, Screenschedule.movie_id == Movie.id)
    movies = movies.filter_by(movie_id=Screenschedule.movie_id).all()
    movie_list = []
    for movie in movies:
        screenschedule_list = []
        screenschedules = Screenschedule.query.filter(Screenschedule.endtime < now + timedelta(days=1)).\
            filter(Screenschedule.movie_id == movie.id).all()
        for screenschedule in screenschedules:
            screenschedule_list.append(dict(id=screenschedule.id, starttime=screenschedule.starttime, endtime=screenschedule.endtime, screen=screenschedule.screen_number))
        movie_list.append(dict(id=movie.id, title=movie.title, age=movie.age, running_time=movie.running_time, genre=movie.genre, screenschedules=screenschedule_list))
 
    return render_template('client_templates/theaters.html', theaters=theaters, date=selected_date, week_list=week_list, now=datetime.now(), movies=movie_list)
    

@bp.route('/<int:theater_id>')
def other(theater_id):
    theaters = Theater.query.get(theater_id)
    week = {0:'월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}
    week_list = []
    now = datetime.now()
    now_weekday = now.weekday()

    args = request.args
    movie_id = args.get('movie_id')
    selected_date = args.get('date', now.strftime('%Y-%m-%d'))
    selected_theater_id = args.get('theater_id')

    for i in range(now_weekday, now_weekday+7):
        day = i - now_weekday
        date = now + timedelta(days=day)
        i %= 7
        week_list.append({'weekday' : week[i], 'date':date.strftime('%Y-%m-%d')})
    
    # 해당 극장에 해당하는 영화만 보여줌
    if selected_theater_id:
        movies = Movie.query.join(Screenschedule, and_(Screenschedule.movie_id == Movie.id, Screenschedule.theater_id == selected_theater_id))
    else:
        movies = Movie.query.join(Screenschedule, Screenschedule.movie_id == Movie.id)
    movies = movies.filter_by(movie_id=Screenschedule.movie_id).all()
    movie_list = []
    for movie in movies:
        screenschedule_list = []
        screenschedules = Screenschedule.query.filter(Screenschedule.endtime < now + timedelta(days=1)).\
            filter(Screenschedule.movie_id == movie.id).all()
        for screenschedule in screenschedules:
            screenschedule_list.append(dict(id=screenschedule.id, starttime=screenschedule.starttime, endtime=screenschedule.endtime, screen=screenschedule.screen_number))
        movie_list.append(dict(id=movie.id, title=movie.title, age=movie.age, running_time=movie.running_time, genre=movie.genre, screenschedules=screenschedule_list))

    return render_template('client_templates/theaters.html', theaters=theaters, date=selected_date, week_list=week_list, now=datetime.now())