import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://admin:eritip18!@database-eritip.cvgx9v3ektbw.ap-northeast-2.rds.amazonaws.com:3306/TheaterDB?charset=utf8'

SQLALCHEMY_TRACK_MODIFICATIONS = False

ALLOWED_HOSTS = ['web']

#이건 나중에 변경해야함 https://wikidocs.net/81052
SECRET_KEY = "dev"