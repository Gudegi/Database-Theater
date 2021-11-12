from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from flex import db
from flex.forms import MemberCreateForm, MemberLoginForm
from flex.models import Member
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup/', methods=('GET', 'POST'))
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
            flash('이미 존재하는 사용자입니다.')
    return render_template('client_templates/auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
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

@bp.before_app_request
def load_logged_in_member():
    member_id = session.get('member_id')
    if member_id is None:
        g.member = None
    else:
        g.member = Member.query.get(member_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view