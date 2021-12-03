from datetime import datetime
from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from .. import db
from ..forms import AnswerForm,NoticeAnswerForm
from ..models import Question, Answer,Notice,NoticeAnswer

bp = Blueprint('answer', __name__, url_prefix='/answer')


@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        question.qsa.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)

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