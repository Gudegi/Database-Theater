from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import datetime
import ast

from flex.models import Movie, Screenschedule, Theater, Actor, Seat, Membership, Coupon, Benefit, IsUsed
from flex.forms import ReservationFirstForm, ReservationSecondForm, ReservationSeatForm, PaymentForm, PaymentCommitForm

bp = Blueprint('reservation', __name__, url_prefix='/ticket')



@bp.route('/')
def ticket():
    movie_list = Movie.query.all()
    return render_template('client_templates/ticket.html',  movie_list = movie_list)


@bp.route('/<int:movie_id>', methods=('GET', 'POST'))
def res_step1(movie_id):
    movie = Movie.query.get(movie_id)
    theater_list = Theater.query.all()
    form = ReservationFirstForm()
    if request.method == 'POST' and form.validate_on_submit():
        # return redirect((url_for('reservation.ticket')))
        # return redirect(url_for('reservation.res_time', theater_name=form.theater_name.data, res_date=form.res_date.data))
        return redirect(url_for('reservation.res_step2', theater_name=form.theater_name.data, res_date=form.res_date.data, movie_id=movie_id))
    return render_template('client_templates/res-step1.html', movie = movie, theater_list = theater_list, form=form)


@bp.route('/<int:movie_id>/<string:res_date>/<string:theater_name>', methods=('POST', 'GET')) # url_for인자로 넘긴것은 무조건 bp에 들어가야함?
def res_step2(theater_name, res_date, movie_id):
    py_res_date = datetime.date.fromisoformat(res_date)
    schedule_list = Screenschedule.query.filter(Theater.name == theater_name,  Screenschedule.movie_id == movie_id).order_by(Screenschedule.starttime.asc())
    movie = Movie.query.get(movie_id)
    actor_list = Actor.query.filter(Actor.movie_id == movie_id).all()
    form = ReservationSecondForm()
    real_list = []
    for schedule in schedule_list:
        if Screenschedule.query.get(schedule.id).starttime.date() == py_res_date:
            real_list.append(schedule)
    if request.method == 'POST' and form.validate_on_submit():
        # for schedule in real_list :
        #     Screenschedule.query.get(schedule.id).starttime.date() ==

        return redirect(url_for('reservation.seat', movie_id = movie_id, res_date = res_date, theater_name=theater_name, schedule_id = form.res_time.data))
    return render_template('client_templates/res-step2.html', schedule_list=real_list, theater_name= theater_name, res_date = py_res_date,
                           movie = movie, actor_list = actor_list, form = form)



# 좌석
@bp.route('/<int:movie_id>/<string:res_date>/<string:theater_name>/<int:schedule_id>/seat', methods=('POST', 'GET'))
def seat(movie_id, res_date, theater_name, schedule_id):
    movie = Movie.query.get(movie_id)
    schedule = Screenschedule.query.get(schedule_id)
    theater = Theater.query.get(schedule.theater_id)
    seat_list = Seat.query.filter(Seat.schedule_id == schedule_id).order_by( Seat.row.asc(), Seat.col.asc()) #각각 행열로
    form = ReservationSeatForm()
    if request.method == 'POST' and form.validate_on_submit():
        abc = request.form.getlist('res_seats')
        return redirect(url_for('reservation.pay',movie_id = movie_id, res_date = res_date, theater_name = theater_name, schedule_id = schedule_id, seats=abc))
    return render_template('client_templates/seat.html', movie = movie, res_date = res_date, schedule = schedule, theater = theater, seat_list = seat_list, form = form)


@bp.route('/<int:movie_id>/<string:res_date>/<string:theater_name>/<int:schedule_id>/seat/<seats>/pay', methods=('POST','GET'))
def pay(movie_id, res_date, theater_name, schedule_id, seats):
    form = PaymentForm()
    movie = Movie.query.get(movie_id)
    schedule = Screenschedule.query.get(schedule_id)
    theater = Theater.query.get(schedule.theater_id)
    seat_list = []
    x = ast.literal_eval(seats)
    membership_point = 0
    membership_coupon = {}
    bene = Benefit.query.all()
    if g.member:
        membership = Membership.query.get(g.member.membership_id)
        membership_point = membership.point
        isuse = IsUsed.query.filter(IsUsed.membership_id == membership.id, IsUsed.issued == 1).all()
        for item in isuse:
            code = Coupon.query.get(item.coupon_code)
            if code.expiredate > datetime.datetime.now() :
                membership_coupon[item.coupon_code] = code.expiredate
    if isinstance(x, list):
        for seat in x:
            seat_list.append(Seat.query.get(seat))
    else :
        seat_list.append(Seat.query.get(seats))
    if request.method == 'POST' and form.validate_on_submit():
        if membership_point >= form.point.data:
            return redirect((url_for('reservation.last_commit', movie_id = movie_id, res_date = res_date, theater_name = theater_name,
                                     schedule_id = schedule_id, seats=seats, coupon=form.coupon.data, point=form.point.data)))
        else :
            flash("멤버쉽 포인트 : 보유 포인트 내로 작성해주세요")
    return render_template('client_templates/payment.html', schedule = schedule, movie = movie, theater = theater, test = seat_list,
                           point = membership_point, coupon = membership_coupon, bene=bene, form=form)


@bp.route('/<int:movie_id>/<string:res_date>/<string:theater_name>/<int:schedule_id>/seat/<seats>/pay/commit/<coupon>/<int:point>', methods=('POST', 'GET'))
def last_commit(movie_id, res_date, theater_name, schedule_id, seats, coupon, point):
    movie = Movie.query.get(movie_id)
    form = PaymentCommitForm()
    schedule = Screenschedule.query.get(schedule_id)
    screen_number = schedule.screen_number
    date = schedule.starttime
    membership = Membership.query.get(g.member.membership_id)
    x = ast.literal_eval(seats)
    total_seat_price = 0
    seat_list = []
    if isinstance(x, list):
        for seat in x:
            seat_list.append(Seat.query.get(seat))
    else :
        seat_list.append(Seat.query.get(seats))
    # 총가격 계산
    for seat in seat_list:
        total_seat_price += int(seat.price)
    # coupon이 "-1" 이 아니면
    # if coupon != "-1":


    # form에서 reservation, pay, discount를

    return render_template('client_templates/pay-commit.html', theater_name = theater_name, schedule = schedule,
                           coupon = coupon, point = point, seat_price = total_seat_price, seat_list =seat_list, movie=movie)