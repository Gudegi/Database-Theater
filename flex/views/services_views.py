from datetime import datetime

from flask import Blueprint, render_template, request, url_for,g,flash
from werkzeug.utils import redirect

from .. import db
from flex.models import Notice,Inquiry,InquiryAnswer,NoticeAnswer,Question,Answer
from ..forms import QuestionForm, AnswerForm,NoticeForm,NoticeAnswerForm
from .auth_views import login_required
bp = Blueprint('services', __name__, url_prefix='/services')

@bp.route('/')
def _select():

    return render_template('services/services_select.html')




@bp.route('/notice/')
def _notice():
    page = request.args.get('page', type=int, default=1)
    notice_list = Notice.query.order_by(Notice.date.desc())
    notice_list = notice_list.paginate(page, per_page=10)
    return render_template('services/services_notice_list.html', notice_list=notice_list)

@bp.route('/notice/create/', methods=('GET', 'POST'))
def noticeCreate():
    form = NoticeForm()
    if request.method == 'POST' and form.validate_on_submit():
        notice = Notice(title=form.subject.data, content=form.content.data, date=datetime.now(), theater_id = 1)
        db.session.add(notice)
        db.session.commit()
        return redirect(url_for('services._notice'))
    return render_template('question/notice_form.html', form=form)

@bp.route('/notice/<int:notice_id>/')
def noticeDetail(notice_id):
    form = NoticeAnswerForm()
    notice = Notice.query.get_or_404(notice_id)
    return render_template('question/notice_detail.html', notice = notice, form=form)




@bp.route('/inquiry/')
def _inquiry():
    page = request.args.get('page', type=int, default=1)
    inquiry_list = Inquiry.query.order_by(Inquiry.date.desc())
    inquiry_list = inquiry_list.paginate(page, per_page=10)
    return render_template('services/services_question_list.html', inquiry_list=inquiry_list)



@bp.route('/inquiry/create/', methods=('GET', 'POST'))
@login_required
def inquiryCreate():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        inquiry = Inquiry(title=form.subject.data, content=form.content.data, date=datetime.now(),member_id = g.member.id)
        db.session.add(inquiry)
        db.session.commit()
        return redirect(url_for('services._inquiry'))
    return render_template('question/question_form.html', form=form)


@bp.route('/inquiry/<int:inquiry_id>/')
def inquiryDetail(inquiry_id):
    form = AnswerForm()
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    return render_template('question/question_detail.html', inquiry=inquiry, form=form)

@bp.route('/delete/<int:inquiry_id>')
@login_required
def inquiryDelete(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    if g.member.id != inquiry.member_id:
        flash('삭제권한이 없습니다')
        return redirect(url_for('services.inquiryDetail', inquiry_id=inquiry_id))
    db.session.delete(inquiry)
    db.session.commit()
    return redirect(url_for('services._inquiry'))