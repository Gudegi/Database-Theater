from datetime import datetime

from flask import Blueprint, render_template, request, url_for,g
from werkzeug.utils import redirect

from .. import db
from flex.models import Notice,Question,Answer,NoticeAnswer
from ..forms import QuestionForm, AnswerForm,NoticeForm,NoticeAnswerForm

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
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template('services/services_question_list.html', question_list=question_list)



@bp.route('/inquiry/create/', methods=('GET', 'POST'))
def inquiryCreate():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),member_id= 0  )
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('services._inquiry'))
    return render_template('question/question_form.html', form=form)


@bp.route('/inquiry/<int:question_id>/')
def inquiryDetail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)