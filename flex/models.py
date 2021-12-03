from sqlalchemy.orm import backref, relationship
from flex import db
from flask_security import RoleMixin, UserMixin


# foreignkey와 primary_key에는 nullable 값 따로 지정 X


class Coupon(db.Model):
    code = db.Column(db.String(20), primary_key=True)
    expiredate = db.Column(db.DateTime, nullable=False)


class Inquiry(db.Model):
    number = db.Column(db.Integer, primary_key=True)  # int?
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))


class InquiryAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    inquiry_id = db.Column(db.Integer, db.ForeignKey('inquiry.number', ondelete='CASCADE'))
    inquiry = db.relationship('Inquiry', backref=db.backref('inquiry'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45), nullable=False)
    eng_title = db.Column(db.String(45), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    director = db.Column(db.String(20), nullable=False)
    running_time = db.Column(db.Integer, nullable=False)
    information = db.Column(db.String(255), nullable=False)
    release = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(20), nullable=False)
    language = db.Column(db.String(20), nullable=False)

    def __str__(self):
        return self.title


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    name = db.Column(db.String(255), nullable=False)
    # backref를 이용
    # movie = db.relationship('Movie', backref=db.backref('answer_set'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    rate = db.Column(db.Integer, nullable=False)  # float에서 int로 변경
    date = db.Column(db.DateTime, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # ondelete='CASCADE' 필요 없지 않나?
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))
    modify_date = db.Column(db.DateTime)
    sentiment = db.Column(db.Integer)


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(20), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))


class Member(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)  # 이름 속성 누락 추가
    pw = db.Column(db.String(200), nullable=False)  # pw 암호화를 위해 20 => 200byte 변경
    birth_date = db.Column(db.Date, nullable=False)  # emplyoee와 통일성을 위한 언더바 추가
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'))


class IsUsed(db.Model):
    membership_id = db.Column(db.Integer, db.ForeignKey('membership.id'), primary_key=True)
    coupon_code = db.Column(db.String(20), db.ForeignKey('coupon.code'), primary_key=True)  # 쿠폰이 삭제되면 같이 삭제?
    issued = db.Column(db.Integer, nullable=False)


class Benefit(db.Model):
    coupon_code = db.Column(db.String(20), db.ForeignKey('coupon.code'), primary_key=True)
    benefit = db.Column(db.Integer(), nullable=False)


class Discount(db.Model):
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'), primary_key=True)
    pay_number = db.Column(db.Integer, db.ForeignKey('pay.number'), primary_key=True)
    pay_reservation_id = db.Column(db.Integer, db.ForeignKey('pay.reservation_id'), primary_key=True)
    discount_amount = db.Column(db.Integer)


class Pay(db.Model):
    number = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstpay = db.Column(db.Integer, nullable=False)  # _추가
    coupon_code = db.Column(db.String(20), nullable=False)  # _추가
    used_points = db.Column(db.Integer, nullable=False)  # _추가
    method = db.Column(db.String(20), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))


class Cancel(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    cancelpay = db.Column(db.Integer, nullable=False)  # _추가
    datetime = db.Column(db.DateTime, nullable=False)
    pay_number = db.Column(db.Integer, db.ForeignKey('pay.number'))
    res_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))


class Nonmember(db.Model):
    phone = db.Column(db.String(11), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    pw = db.Column(db.String(200), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)  # 통일성을 위한 언더바 추가


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    screen_schedule_id = db.Column(db.Integer, db.ForeignKey('screenschedule.id'))
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))
    nonmember_phone = db.Column(db.String(11), db.ForeignKey('nonmember.phone'))
    seats = db.Column(db.String(1000), nullable=False)
    seat_screen_number = db.Column(db.Integer, db.ForeignKey('seat.screen_number'))


class Screenschedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session = db.Column(db.Integer, nullable=False)
    starttime = db.Column(db.DateTime, nullable=False)  # _추가
    endtime = db.Column(db.DateTime, nullable=False)  # _추가
    screen_number = db.Column(db.Integer, db.ForeignKey('screen.number'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))
    theater = db.relationship('Theater', backref=db.backref('theater_names'))  # 어드민 페이지 위한 역참조
    title = db.relationship('Movie', backref=db.backref('titles'))  # 어드민 페이지 위한 역참조
    screen = db.relationship('Screen', backref=db.backref('screen_names'))  # 어드민 페이지 위한 역참조

    def __str__(self):
        return self.theater_id


class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    tel = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(50), nullable=False)  # 추가
    seat = db.Column(db.Integer, nullable=False)  # 추가
    screen = db.Column(db.Integer, nullable=False)  # 추가
    representive = db.Column(db.String(10), nullable=False)

    def __str__(self):
        return self.name


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))
    theater = db.relationship('Theater', backref=db.backref('theater_names2'))


class NoticeAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notice_id = db.Column(db.Integer, db.ForeignKey('notice.id', ondelete='CASCADE'))
    notice = db.relationship('Notice', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Screen(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    seat = db.Column(db.Integer, nullable=False)  # 추가
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))  # 추가, 상영관은 영화관 참조

    def __str__(self):
        return self.name


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    row = db.Column(db.String(1), nullable=False)
    col = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    screen_number = db.Column(db.Integer, db.ForeignKey('screen.number'))
    schedule_id = db.Column(db.Integer, db.ForeignKey('screenschedule.id'))


# 아래부터 직원파트

class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    place = db.Column(db.String(45), nullable=False)
    installdate = db.Column(db.DateTime, nullable=False)  # _추가
    inspectiondate = db.Column(db.DateTime, nullable=False)  # _추가
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))


class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))


class Subfacility(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.String(11), nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    subfacility_id = db.Column(db.Integer, db.ForeignKey('subfacility.id'))


class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    score = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(45), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def userName(self):
        return self.user

    @property
    def userTheater(self):
        return self.user.theater


class Commute(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    starttime = db.Column(db.DateTime, nullable=False)  # _추가
    endtime = db.Column(db.DateTime, nullable=False)  # _ 추가
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user_name'))  # 어드민 페이지 역참조

    @property
    def work_time(self):
        # 일한 시간
        return self.endtime - self.starttime


class Schedulemanage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# 이 아래는 Pybo 원본
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    def __str__(self):
        return self.content


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('qsa'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    @property
    def questionSubject(self):
        return self.question.subject

    @property
    def questionContent(self):
        return self.question.content


# adminLTE####################
# Define models

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    # name = db.relationship('User', secondary = roles_users, back_populates="roles")
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    active = db.Column(db.Boolean())
    salary = db.Column(db.Integer, nullable=False)
    account = db.Column(db.String(20), nullable=False)
    department_info = db.Column(db.String(20))  # 변경 예정 department_info > position
    confirmed_at = db.Column(db.DateTime())
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id'))
    theater = db.relationship('Theater', backref=db.backref('theater2'))

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('roles', lazy='dynamic'))

    def __str__(self):
        '''attrs = db.class_mapper(self.__class__).attrs

        if 'first_name' in attrs:
            name = self.last_name + self.first_name
            return str(name)

        if 'theater' in attrs:
            return str(self.theater)'''
        name = self.last_name + self.first_name
        return str(name)

    @property
    def userName(self):
        name = self.last_name + self.first_name
        return str(name)

    # admin_views에서 self.roles만 가져다 쓰면 <Role 1> 이렇게 밖에 못씀. 여기서 리턴 바꿔줘야함
    @property
    def role_name(self):
        # 한 행(직원)씩 리턴 직원 6명이면 6번 return
        lis = []
        for i in self.roles:
            lis.append(i.name)
        return lis