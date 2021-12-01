from flask import Blueprint, url_for, render_template, flash, request, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import datetime

from flex import db
from flex.models import Movie, Screenschedule, Theater, Actor, Seat, Membership, Coupon, Benefit, IsUsed, Reservation, Pay, IsUsed, Screen, Cancel
from flex.forms import ReservationCancelForm

bp = Blueprint('mypage', __name__, url_prefix='/mypage')

@bp.route('/')
def mypage():
    member_id = -1
    if g.member:
        member_id = g.member.id
    else :
        return redirect(url_for('main.init')) #로그인 안한상태면 메인화면으로 보냄.
    res_list = Reservation.query.filter(Reservation.member_id == member_id).all()
    history_list = []
    future_list = []

    for i in range(len(res_list)):
        this_list = []
        this_schedule = Screenschedule.query.get(res_list[i].screen_schedule_id)
        if len(Cancel.query.filter(Cancel.res_id == res_list[i].id).all()) == 0: # 취소가 안된 영화만
            this_list.append(res_list[i])  # list[][0] Reservation
            this_list.append(Movie.query.get(this_schedule.movie_id))  # list[][1] Movie
            this_list.append(this_schedule)  # list[0][2] Schedule
            seat_list = res_list[i].seats.split()
            query_seat_list = []
            for j in range(len(seat_list)):
                seat = Seat.query.get(seat_list[j])
                query_seat_list.append(seat)
            this_list.append(query_seat_list)
            this_list.append(Theater.query.get(this_schedule.theater_id))
            this_list.append(Screen.query.get(this_schedule.screen_number))
            if this_schedule.starttime > datetime.datetime.now():
                future_list.append(this_list)
            else:
                history_list.append(this_list)
    history_num = len(history_list)
    future_num = len(future_list)
    return render_template('client_templates/reservation-check.html', future_list=future_list, history_list=history_list,
                           history_num=history_num, future_num=future_num)


@bp.route('/<int:res_id>', methods=('POST', 'GET'))
def cancel(res_id):
    member_id = -1
    if g.member:
        member_id = g.member.id
    else:
        return redirect(url_for('main.init'))  # 로그인 안한상태면 메인화면으로 보냄.
    reservation = Reservation.query.get(res_id)
    schedule = Screenschedule.query.get(reservation.screen_schedule_id)
    movie = Movie.query.get(schedule.movie_id)
    membership = Membership.query.filter(Membership.member_id == member_id).first()
    screen = Screen.query.get(schedule.screen_number)
    pay = Pay.query.filter(Pay.reservation_id == res_id).first()
    seat_list = reservation.seats.split()
    theater_name = Theater.query.get(schedule.theater_id)
    query_seat_list = []
    coupon_value = 0
    form = ReservationCancelForm()
    if pay.coupon_code != "-1":
        coupon_value = Benefit.query.get(pay.coupon_code).benefit
    for j in range(len(seat_list)):
        seat = Seat.query.get(seat_list[j])
        query_seat_list.append(seat)
    if request.method == 'POST' and form.validate_on_submit():
        if pay.coupon_code != "-1":
            is_used = IsUsed.query.filter(IsUsed.membership_id == membership.id, IsUsed.coupon_code == pay.coupon_code).first()
            is_used.issued = 0
            db.session.add(is_used)
        for seat in query_seat_list:
            seat.available=1
            db.session.add(seat)
        cancel = Cancel(cancelpay=pay.firstpay,
                        datetime=datetime.datetime.now(),
                        pay_number=pay.number,
                        res_id=reservation.id)
        membership.point += pay.used_points
        db.session.add(cancel)
        db.session.commit()
        return redirect((url_for('mypage.mypage')))
    return render_template('client_templates/cancel-reservation.html', reservation = reservation, schedule = schedule, movie = movie,
                           pay = pay, query_seat_list = query_seat_list, theater_name=theater_name, screen=screen, coupon_value = coupon_value, form=form)