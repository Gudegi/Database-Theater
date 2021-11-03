from flex import db
from flask_security import RoleMixin, UserMixin
# foreignkey와 primary_key에는 nullable 값 따로 지정 X


class Coupon(db.Model):
    code = db.Column(db.String(20), primary_key=True)
    expiredate = db.Column(db.DateTime, nullable=False)


class Inquiry(db.Model):
    number = db.Column(db.Integer, primary_key=True) # int?
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))


class Movie(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    director = db.Column(db.String(20), nullable=False)
    running_time = db.Column(db.Integer, nullable=False)
    information = db.Column(db.String(255), nullable=False)


class Review(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    movie_id = db.Column(db.String(20), db.ForeignKey('movie.id')) # ondelete='CASCADE' 필요 없지 않나?
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))


class Membership(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    rank = db.Column(db.String(20), nullable=False)
    point = db.Column(db.Integer, nullable=False)
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))


class Member(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    pw = db.Column(db.String(200), nullable=False) # pw 암호화를 위한 글자수 200 설정
    birth_date = db.Column(db.Date, nullable=False) # emplyoee와 통일성을 위한 언더바 추가
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    membership_id = db.Column(db.String(20), db.ForeignKey('membership.id'))


class IsUsed(db.Model):
    membership_id = db.Column(db.String(20), db.ForeignKey('membership.id'), primary_key=True)
    coupon_code = db.Column(db.String(20), db.ForeignKey('coupon.code'), primary_key=True) # 쿠폰이 삭제되면 같이 삭제?
    issued = db.Column(db.Integer, nullable=False)


# coupon_code, benefit 둘다 PK가 맞는지?
class Benefit(db.Model):
    coupon_code = db.Column(db.String(20), db.ForeignKey('coupon.code'), primary_key=True)
    benefit = db.Column(db.String(20), primary_key=True)


class Discount(db.Model):
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'), primary_key=True)
    pay_number = db.Column(db.Integer, db.ForeignKey('pay.number'), primary_key=True)
    pay_reservation_id = db.Column(db.String(20), db.ForeignKey('pay.reservation_id'), primary_key=True)
    discount_amount = db.Column(db.Integer)


class Pay(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    firstpay = db.Column(db.Integer, nullable=False) # _추가
    discountpay = db.Column(db.Integer, nullable=False) # _추가
    lastpay = db.Column(db.Integer, nullable=False) # _추가
    method = db.Column(db.String(20), nullable=False)
    reservation_id = db.Column(db.String(20), db.ForeignKey('reservation.id'))


class Cancel(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    cancelpay = db.Column(db.Integer, nullable=False) # _추가
    usingcoupon = db.Column(db.Integer, nullable=False) # _ 추가
    datetime = db.Column(db.DateTime, nullable=False)
    pay_number = db.Column(db.Integer, db.ForeignKey('pay.number'))


class Nonmember(db.Model):
    phone = db.Column(db.String(11),primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    pw = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False) #통일성을 위한 언더바 추가


class Reservation(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    screen_schedule_id = db.Column(db.String(20), db.ForeignKey('screenschedule.id'))
    member_id = db.Column(db.String(20), db.ForeignKey('member.id'))
    nonmember_phone = db.Column(db.String(11), db.ForeignKey('nonmember.phone'))
    movie_id = db.Column(db.String(20), nullable=False)
    seat_number = db.Column(db.String(10), db.ForeignKey('seat.number'))
    seat_screen_number = db.Column(db.Integer, db.ForeignKey('seat.screen_number'))


class Screenschedule(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    session = db.Column(db.String(45), nullable=False)
    starttime = db.Column(db.DateTime, nullable=False) #_추가
    endtime = db.Column(db.DateTime, nullable=False) # _추가
    screen_number = db.Column(db.Integer, db.ForeignKey('screen.number'))
    movie_id = db.Column(db.String(20), db.ForeignKey('movie.id'))
    theater_id = db.Column(db.String(20), db.ForeignKey('theater.id'))


class Theater(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    tel = db.Column(db.String(11), nullable=False)
    representive = db.Column(db.String(10), nullable=False)


class Notice(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    theater_id = db.Column(db.String(20), db.ForeignKey('theater.id'))


class Screen(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)


class Seat(db.Model):
    number = db.Column(db.String(10), primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    available = db.Column(db.Integer, nullable=False)
    seatprice = db.Column(db.Integer, nullable=False) # _추가
    screen_number = db.Column(db.Integer, db.ForeignKey('screen.number'))


# 아래부터 직원파트

class Facility(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    place = db.Column(db.String(45), nullable=False)
    installdate = db.Column(db.DateTime, nullable=False) # _추가
    inspectiondate = db.Column(db.DateTime, nullable=False) # _추가
    theater_id = db.Column(db.String(20), db.ForeignKey('theater.id'))


class Equipment(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)
    theater_id = db.Column(db.String(20), db.ForeignKey('theater.id'))


class Subfacility(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    tel = db.Column(db.String(11), nullable=False)
    theater_id = db.Column(db.String(20), db.ForeignKey('theater.id'))


class Product(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    subfacility_id = db.Column(db.String(20), db.ForeignKey('subfacility.id'))


class Info(db.Model):
    department = db.Column(db.String(20), primary_key=True)
    position = db.Column(db.String(25), primary_key=True)
    authority = db.Column(db.String(30))


class Employee(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    pw = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    account = db.Column(db.String(20), nullable=False)
    theater_id = db.Column(db.String(20), db.ForeignKey('theater.id'))
    # department_info = db.Column(db.String(20), db.ForeignKey('info.department'))
    # position_info = db.Column(db.String(25), db.ForeignKey('info.position'))
    # author_info = db.Column(db.String(30), db.ForeignKey('info.authority'))
    # adminLte 사용에 따라 일단 주석 처리.

class Evaluation(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    score = db.Column(db.Integer(), nullable=False)
    comment = db.Column(db.String(45), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'))


class Commute(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    starttime = db.Column(db.DateTime, nullable=False) # _추가
    endtime = db.Column(db.DateTime, nullable=False) # _ 추가
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'))


class Schedulemanage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    employee_id = db.Column(db.String(20), db.ForeignKey('employee.id'))


# 이 아래는 Pybo 원본
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

#adminLTE####################
# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


    def __str__(self):
        return self.first_name + " " + self.last_name + " <" + self.email + ">"