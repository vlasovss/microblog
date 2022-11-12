from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

from config import Config

# App
app = Flask(__name__)
app.config.from_object(Config)

if not app.debug:
    # Sending errors by email.
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no_reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], 
            subject='Microblog Failure',
            credentials=auth,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
    # Writing a log to a file
    logs_dir = Path('logs')
    if not logs_dir.exists():
        logs_dir.mkdir()
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

# Mail
mail = Mail(app)

# Login
login = LoginManager(app)
login.login_view = 'login'

# DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors