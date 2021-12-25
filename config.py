import os

BASE_DIR = os.path.dirname(__file__)

#github public 배포 과정에 보안상 RDS 비밀번호를 교체하였습니다. 첨부한 sqlite와 sql을 이용해주세요.
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:970925as!@database-eritip.cvgx9v3ektbw.ap-northeast-2.rds.amazonaws.com:3306/TheaterDB?charset=utf8'
#MariaDB > sqlite 과정에 코드 호환이 안되는 부분이 있습니다. 맞게 고쳐주셔야 실행됩니다.
DATABASE_FILE = 'TheaterDB_2021-12-25.sqlite'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, DATABASE_FILE))
SQLALCHEMY_ECHO = True


SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_HOSTS = ['web']

SECRET_KEY = "dev"


######adminLTE#######
# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"

# Flask-Security features
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False