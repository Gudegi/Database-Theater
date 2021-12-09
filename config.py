import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:eritip18!@database-eritip.cvgx9v3ektbw.ap-northeast-2.rds.amazonaws.com:3306/TheaterDB?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_HOSTS = ['web']

#이건 나중에 변경해야함 https://wikidocs.net/81052
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