from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import datetime
import ast

from flex import db
from flex.models import Movie, Screenschedule, Theater, Actor, Seat, Membership, Coupon, Benefit, IsUsed, Reservation, Screen, \
    Pay, IsUsed, Review
from flex.forms import ReservationFirstForm, ReservationSecondForm, ReservationSeatForm, PaymentForm, PaymentCommitForm

bp = Blueprint('reservation', __name__, url_prefix='/ticket')


@bp.route('/')
def ticket():
    movie_list = Movie.query.order_by(Movie.id.asc())
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
    return render_template('client_templates/ticket.html', rate_list=rate_list)


@bp.route('/<int:movie_id>', methods=('GET', 'POST'))
def res_step1(movie_id):
    movie = Movie.query.get(movie_id)
    theater_list = Theater.query.all()
    review_list = Review.query.filter(Review.movie_id == movie_id).all()
    sum = 0
    for review in review_list:
        sum += review.rate
    if len(review_list) != 0:
        rate = round(sum / len(review_list),2)
    else:
        rate = 0
    form = ReservationFirstForm()
    if request.method == 'POST' and form.validate_on_submit():
        # return redirect((url_for('reservation.ticket')))
        # return redirect(url_for('reservation.res_time', theater_name=form.theater_name.data, res_date=form.res_date.data))
        return redirect(
            url_for('reservation.res_step2', theater_name=form.theater_name.data, res_date=form.res_date.data,
                    movie_id=movie_id))
    return render_template('client_templates/res-step1.html', movie=movie, theater_list=theater_list, form=form, rate=rate)


@bp.route('/<int:movie_id>/<string:res_date>/<int:theater_name>',
          methods=('POST', 'GET'))  # url_for????????? ???????????? ????????? bp??? ????????????????
def res_step2(theater_name, res_date, movie_id):
    theater = Theater.query.get(theater_name)
    py_res_date = datetime.date.fromisoformat(res_date)
    schedule_list = Screenschedule.query.filter(Screenschedule.theater_id == theater.id,
                                                Screenschedule.movie_id == movie_id).order_by(Screenschedule.starttime.asc())
    movie = Movie.query.get(movie_id)
    actor_list = Actor.query.filter(Actor.movie_id == movie_id).all()
    form = ReservationSecondForm()
    real_list = []
    for schedule in schedule_list:
        if schedule.starttime.date() == py_res_date and schedule.starttime > datetime.datetime.now():
            real_list.append(schedule)
    if request.method == 'POST' and form.validate_on_submit():
        # for schedule in real_list :
        #     Screenschedule.query.get(schedule.id).starttime.date() ==

        return redirect(url_for('reservation.seat', movie_id=movie_id, res_date=res_date, theater_name=theater_name,
                                schedule_id=form.res_time.data))
    return render_template('client_templates/res-step2.html', schedule_list=real_list, theater=theater,
                           res_date=py_res_date,
                           movie=movie, actor_list=actor_list, form=form)


# ??????
@bp.route('/<int:movie_id>/<string:res_date>/<int:theater_name>/<int:schedule_id>/seat', methods=('POST', 'GET'))
def seat(movie_id, res_date, theater_name, schedule_id):
    movie = Movie.query.get(movie_id)
    schedule = Screenschedule.query.get(schedule_id)
    screen = Screen.query.get(schedule.screen_number)
    theater = Theater.query.get(schedule.theater_id)
    seat_list = Seat.query.filter(Seat.schedule_id == schedule_id).order_by(Seat.row.asc(), Seat.col.asc())  # ?????? ?????????
    form = ReservationSeatForm()
    if request.method == 'POST' and form.validate_on_submit():
        abc = request.form.getlist('res_seats')
        return redirect(url_for('reservation.pay', movie_id=movie_id, res_date=res_date, theater_name=theater_name,
                                schedule_id=schedule_id, seats=abc))
    return render_template('client_templates/seat.html', movie=movie, res_date=res_date, schedule=schedule,
                           theater=theater, seat_list=seat_list, form=form, screen=screen)


@bp.route('/<int:movie_id>/<string:res_date>/<int:theater_name>/<int:schedule_id>/seat/<seats>/pay',
          methods=('POST', 'GET'))
def pay(movie_id, res_date, theater_name, schedule_id, seats):
    form = PaymentForm()
    movie = Movie.query.get(movie_id)
    schedule = Screenschedule.query.get(schedule_id)
    theater = Theater.query.get(schedule.theater_id)
    screen = Screen.query.get(schedule.screen_number)
    seat_list = []
    x = ast.literal_eval(seats)
    membership_point = 0
    membership_coupon = {}
    bene = Benefit.query.all()
    if g.member:
        membership = Membership.query.get(g.member.membership_id)
        membership_point = membership.point
        isuse = IsUsed.query.filter(IsUsed.membership_id == membership.id, IsUsed.issued == 0).all()
        for item in isuse:
            code = Coupon.query.get(item.coupon_code)
            if code.expiredate > datetime.datetime.now():
                membership_coupon[item.coupon_code] = code.expiredate
        if isinstance(x, list):
            for seat in x:
                seat_list.append(Seat.query.get(seat))
        else:
            seat_list.append(Seat.query.get(seats))
        if request.method == 'POST' and form.validate_on_submit():
            if membership_point >= form.point.data:
                return redirect(
                    (url_for('reservation.last_commit', movie_id=movie_id, res_date=res_date, theater_name=theater_name,
                            schedule_id=schedule_id, seats=seats, coupon=form.coupon.data, point=form.point.data)))
            else:
                flash("????????? ????????? : ?????? ????????? ?????? ??????????????????")
        
    elif g.guest:
        if isinstance(x, list):
            for seat in x:
                seat_list.append(Seat.query.get(seat))
        else:
            seat_list.append(Seat.query.get(seats))

        if request.method == 'POST' :
            return redirect(
                (url_for('reservation.last_commit', movie_id=movie_id, res_date=res_date, theater_name=theater_name,
                            schedule_id=schedule_id, seats=seats, coupon=0, point=0)))                
    return render_template('client_templates/payment.html', schedule=schedule, movie=movie, theater=theater,
                           test=seat_list,
                           point=membership_point, coupon=membership_coupon, bene=bene, form=form, screen=screen)


@bp.route(
    '/<int:movie_id>/<string:res_date>/<int:theater_name>/<int:schedule_id>/seat/<seats>/pay/commit/<coupon>/<int:point>',
    methods=('POST', 'GET'))
def last_commit(movie_id, res_date, theater_name, schedule_id, seats, coupon, point):
    movie = Movie.query.get(movie_id)
    form = PaymentCommitForm()
    theater = Theater.query.get(theater_name)
    schedule = Screenschedule.query.get(schedule_id)
    screen = Screen.query.get(schedule.screen_number)
    date = schedule.starttime
    bene = Benefit.query.all()
    x = ast.literal_eval(seats)
    total_seat_price = 0
    seat_list = []
    member_id = -1
    seats_string = ""
    is_used = -1
    if g.member:
        membership = Membership.query.get(g.member.membership_id)
        member_id = g.member.id
    
    elif g.guest:
        guest_phone = g.guest.phone

    if isinstance(x, list):
        for seat in x:
            seat_list.append(Seat.query.get(seat))
    else:
        seat_list.append(Seat.query.get(seats))
    # ????????? ??????
    for seat in seat_list:
        total_seat_price += int(seat.price)
        seats_string = seats_string + str(seat.id) + " "
    if request.method == 'POST' and form.validate_on_submit():
        already_reserved = False  # ???????????? ????????? ?????? ????????? ?????? ???????????? ????????????.
        for seat in seat_list:
            if Seat.query.get(seat.id).available == 0:
                already_reserved = True
        if g.member:
            if already_reserved == False:
                reservation = Reservation(date=datetime.datetime.now(),
                                        screen_schedule_id=schedule_id,
                                        member_id=member_id,
                                        seats=seats_string,
                                        seat_screen_number=schedule.screen_number
                                        )
                db.session.add(reservation)
                db.session.commit()  # reservation id??? ??????????????? ??????
                for seat in seat_list:
                    seat.available = 0
                pay = Pay(firstpay=total_seat_price,
                        coupon_code=coupon,
                        used_points=point,
                        method="card",
                        reservation_id=reservation.id
                        )
                membership.point -= point
                if coupon != "-1":
                    is_used = IsUsed.query.filter(IsUsed.membership_id == membership.id, IsUsed.coupon_code == coupon).all()
                    is_used[0].issued = 1
                db.session.add(pay)
                db.session.add(membership)
                db.session.commit()
                return redirect((url_for('reservation.ticket')))
            else:
                return redirect((url_for('main.init404')))
        # ????????? ????????? ??????, ????????? ?????? ????????????
        elif g.guest:
            if already_reserved == False:
                reservation = Reservation(date=datetime.datetime.now(),
                                        screen_schedule_id=schedule_id,
                                        nonmember_phone=guest_phone,
                                        seats=seats_string,
                                        seat_screen_number=schedule.screen_number
                                        )
                db.session.add(reservation)
                db.session.commit()
                for seat in seat_list:
                    seat.available = 0
                pay = Pay(firstpay=total_seat_price,
                        coupon_code=-1,
                        used_points=0,
                        method="card",
                        reservation_id=reservation.id
                        )
                db.session.add(pay)
                db.session.commit()
                return redirect((url_for('reservation.ticket')))
            else:
                return redirect((url_for('main.init404')))
    return render_template('client_templates/pay-commit.html', theater=theater, schedule=schedule,
                           coupon=coupon, point=point, seat_price=total_seat_price, seat_list=seat_list,
                           movie=movie, bene=bene, form=form, seats_string=seats_string, isused=is_used, screen=screen)



@bp.after_request
def add_header(resp):
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp
