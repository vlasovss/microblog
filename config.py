from os import getenv
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent

env_file = Path('.env')
if env_file.exists():
    load_dotenv(env_file)


class Config(object):
    # App
    SECRET_KEY = getenv('SECRET_KEY') or 'you-will-never-guess'
    
    # DB
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL') or \
        'sqlite:///' + str(basedir / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = int(getenv('MAIL_PORT') or  25)
    MAIL_USE_TLS = getenv('MAIL_USE_TLS') is not None
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    ADMINS = ['vlasov.sergey.rf@mail.ru']
    
    # Pagination
    POSTS_PER_PAGE = 10
    
    # Babel
    LANGUAGES = ['en', 'ru']
    
    # Elasticsearch
    ES_URL = getenv('ES_URL')
    ES_LOGIN = getenv('ES_LOGIN')
    ES_PASSWORD = getenv('ES_PASSWORD')