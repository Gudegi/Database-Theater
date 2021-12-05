from datetime import datetime
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm,NoticeAnswerForm
from ..models import Notice,NoticeAnswer,InquiryAnswer,Inquiry

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:inquiry_id>', methods=('POST',))
def create(inquiry_id):
    form = AnswerForm()
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = InquiryAnswer(content=content, create_date=datetime.now())
        inquiry.inquiry.append(answer)
        db.session.commit()
        return redirect(url_for('services.inquiryDetail', inquiry_id=inquiry_id))
    return render_template('question/question_detail.html', inquiry=inquiry, form=form)

@bp.route('/noticeCreate/<int:notice_id>', methods=('POST',))
def noticeCreate(notice_id):
    form = NoticeAnswerForm()
    notice = Notice.query.get_or_404(notice_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = NoticeAnswer(content=content, create_date=datetime.now())
        notice.nsa.append(answer)
        db.session.commit()
        return redirect(url_for('services.noticeDetail', notice_id=notice_id))
    return render_template('question/notice_detail.html', notice=notice, form=form)