from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from flex import db
from flex.forms import MemberCreateForm, MemberLoginForm, NonmemberLoginForm, NonmemberReservationForm
from flex.models import Member, Nonmember, Reservation, Movie, Screenschedule, Theater
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    form = MemberCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        member = Member.query.filter_by(id=form.id.data).first()
        if not member:
            member = Member(id=form.id.data,
                            pw=generate_password_hash(form.password1.data),
                            birth_date=form.birth_date.data,
                            name=form.name.data,
                            phone=form.phone.data,
                            email=form.email.data,
                            nickname=form.nickname.data)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 가입된 사용자입니다.')
    return render_template('client_templates/auth/signup.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = MemberLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        member = Member.query.filter_by(id=form.id.data).first()
        if not member:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(member.pw, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['member_id'] = member.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('client_templates/auth/login.html', form=form)

@bp.route('/guest', methods=('GET', 'POST'))
def guest_login():
    form = NonmemberLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        guest = Nonmember.query.filter_by(phone=form.phone.data).first()
        if not guest:
            guest = Nonmember(phone=form.phone.data,
                              name=form.name.data,
                              pw=generate_password_hash(form.password.data),
                              birth_date=form.birth_date.data)                
            db.session.add(guest)
            db.session.commit()
            session.clear()
            session['nonmember_phone'] = guest.phone
        else:
            guest.pw = generate_password_hash(form.password.data)
            db.session.commit()
            session.clear()
            session['nonmember_phone'] = guest.phone
        return redirect(url_for('main.index'))
    return render_template('client_templates/auth/guest.html', form=form)

@bp.route('/guest/reservation', methods=('GET', 'POST'))
def guest_reservation():
    form = NonmemberReservationForm()
    reservations = []
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        guest = Nonmember.query.filter_by(phone=form.phone.data).first()
        if not guest:
            error = "예매내역이 존재하지 않는 사용자입니다."
        elif not check_password_hash(guest.pw, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        elif (guest.birth_date != form.birth_date.data) :
            error = "생년월일이 올바르지 않습니다."
        else:
            reservations = Reservation.query.join(Screenschedule).filter(Reservation.nonmember_phone == guest.phone).all()
            reservation_list = []
            for reservation in reservations:
                screenschedule_list = []
                screenschedules = Screenschedule.query.filter(Screenschedule.id == reservation.screen_schedule_id).all()
                for screenschedule in screenschedules :
                    movies = Movie.query.filter(Movie.id == screenschedule.movie_id).all()
                    theaters = Theater.query.filter(Theater.id == screenschedule.theater_id).all()
                    screenschedule_list.append(dict(id=screenschedule.id, session=screenschedule.session, starttime=screenschedule.starttime, endtime=screenschedule.endtime, screen=screenschedule.screen_number, movies=movies, theaters=theaters))
                reservation_list.append(dict(id=reservation.id, date=reservation.date, seats=reservation.seats, screen_number=reservation.seat_screen_number, screenschedules = screenschedule_list))
            return render_template('client_templates/auth/guest_reservationlist.html', reservations=reservation_list)
        flash(error)
    return render_template('client_templates/auth/guest_reservation.html', form=form)

@bp.route('/login/<int:movie_id>/movie', methods=('GET', 'POST'))  # 추가.
def login_movie(movie_id):
    form = MemberLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        member = Member.query.filter_by(id=form.id.data).first()
        if not member:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(member.pw, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['member_id'] = member.id
            return redirect(url_for('movies.detail', movie_id=movie_id))
        flash(error)
    return render_template('client_templates/auth/login.html', form=form)

@bp.before_app_request
def load_logged_in_member():
    member_id = session.get('member_id')
    if member_id is None:
        g.member = None
    else:
        g.member = Member.query.get(member_id)

@bp.before_app_request
def load_logged_in_guest():
    nonmember_phone = session.get('nonmember_phone')
    if nonmember_phone is None:
        g.guest = None
    else:
        g.guest = Nonmember.query.get(nonmember_phone)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# 추가
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.member is None:    # g.user 수정
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view