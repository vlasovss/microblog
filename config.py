import os
from pathlib import Path

basedir = Path(__file__).resolve().parent


class Config(object):
    # App
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or  25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['vlasov.sergey.rf@mail.ru']
    
    # Pagination
    POSTS_PER_PAGE = 3
    
    # Babel
    LANGUAGES = ['en', 'ru']