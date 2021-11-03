from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from flex import db
from flex.forms import UserCreateForm, UserLoginForm
from flex.models import Member

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        member = Member.query.filter_by(id=form.id.data).first()
        if not member:
            member = Member(id=form.id.data,
                            pw=generate_password_hash(form.password1.data),
                            birth_date=form.birth_date.data,
                            phone=form.phone.data,
                            email=form.email.data,
                            nickname=form.nickname.data)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
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
    return render_template('auth/login.html', form=form)