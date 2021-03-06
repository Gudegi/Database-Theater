from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, SubmitField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class NoticeForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class NoticeAnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class MemberCreateForm(FlaskForm):
    id = StringField('아이디', validators=[DataRequired('아이디는 필수입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수입력 항목입니다.'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호를 한번 더 입력해주세요.')])
    name = StringField('이름', validators=[DataRequired('이름은 필수입력 항목입니다.')])
    birth_date = StringField('생년월일', validators=[DataRequired('생년월일은 필수입력 항목입니다.')])
    phone = StringField('휴대전화', validators=[DataRequired('휴대전화는 필수입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수입력 항목입니다.'), Email()])
    nickname = StringField('닉네임', validators=[DataRequired('닉네임은 필수입력 항목입니다.')])


class MemberLoginForm(FlaskForm):
    id = StringField('아이디', validators=[DataRequired("아이디를 입력해주세요."), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired("비밀번호를 입력해주세요.")])

class NonmemberLoginForm(FlaskForm):
    name = StringField('이름', validators=[DataRequired("이름을 입력해주세요.")])
    birth_date = StringField('생년월일', validators=[DataRequired('생년월일을 입력해주세요.'), Length(min=8, max=8)])
    phone = StringField('휴대폰번호', validators=[DataRequired("휴대폰번호를 입력해주세요.")])
    password = PasswordField('비밀번호', validators=[DataRequired("비밀번호를 입력해주세요.")])


class NonmemberReservationForm(FlaskForm):
    birth_date = StringField('생년월일', validators=[DataRequired('생년월일을 입력해주세요.'),Length(min=8, max=8)])
    phone = StringField('휴대폰번호', validators=[DataRequired("휴대폰번호를 입력해주세요.")])
    password = PasswordField('비밀번호', validators=[DataRequired("비밀번호를 입력해주세요.")])
    

class ReservationFirstForm(FlaskForm):
    theater_name = StringField('영화관', validators=[DataRequired('필수입력 항목입니다.')])
    res_date = StringField('예매날짜', validators=[DataRequired(' 필수입력 항목입니다.')])


class ReservationSecondForm(FlaskForm):
    res_time = StringField('예매시간', validators=[DataRequired(' 필수입력 항목입니다.')])


class ReservationSeatForm(FlaskForm):
    res_seats = IntegerField('좌석', validators=[DataRequired(' 필수입력 항목입니다.')])


class PaymentForm(FlaskForm):
    coupon = StringField('쿠폰', validators=[DataRequired(' 필수입력 항목입니다.')])
    point = IntegerField('멤버쉽 포인트', [validators.InputRequired("필수입력 항목입니다."), NumberRange(min=0, message='0 이상의 유효한 값을 입력하세요')] )

class PaymentCommitForm(FlaskForm):
    commit = SubmitField('결제 완료')

class ReservationCancelForm(FlaskForm):
    commit = SubmitField('결제 완료')

class ReviewForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    rate = IntegerField('평가', validators=[DataRequired('점수는 1~10 필수입력 항목입니다.')])

