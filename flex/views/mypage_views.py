from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import datetime

from flex.models import Movie, Screenschedule, Theater, Actor, Seat, Membership, Coupon, Benefit, IsUsed, Reservation, Pay, IsUsed
from flex.forms import ReservationFirstForm, ReservationSecondForm, ReservationSeatForm, PaymentForm, PaymentCommitForm

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
        this_list.append(res_list[i])  # list[][0] Reservation
        this_list.append(Movie.query.get(this_schedule.movie_id))  # list[][1] Movie
        this_list.append(this_schedule)  # list[0][2] Schedule
        seat_list = res_list[i].seats.split()
        query_seat_list = []
        for j in range(len(seat_list)):
            seat = Seat.query.get(seat_list[j])
            query_seat_list.append(seat)
        this_list.append(query_seat_list)

        if this_schedule.starttime > datetime.datetime.now():
            future_list.append(this_list)
        else:
            history_list.append(this_list)
        history_num = len(history_list)
        future_num = len(future_list)
    return render_template('client_templates/reservation-check.html', future_list=future_list, history_list=history_list,
                           history_num=history_num, future_num=future_num)


@bp.route('/<int:res_id>')
def cancel(res_id):
    # 구현
    return