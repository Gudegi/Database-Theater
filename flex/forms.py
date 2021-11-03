from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class MemberCreateForm(FlaskForm):
    id = StringField('사용자 ID', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호를 한번 더 입력해주세요')])
    birth_date = StringField('생년월일', validators=[DataRequired('생년월일은 필수입력 항목입니다.')])
    phone = StringField('핸드폰 번호', validators=[DataRequired('핸드폰 번호는 필수입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수입력 항목입니다.'), Email()])
    nickname = StringField('닉네임', validators=[DataRequired('닉네임은 필수입력 항목입니다.')])

class MemberLoginForm(FlaskForm):
    id = StringField('사용자 ID', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])