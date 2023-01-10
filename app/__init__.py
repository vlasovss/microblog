import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
from pathlib import Path

from elasticsearch import Elasticsearch
from flask import Flask, request
from flask import current_app
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
import rq

from config import Config, basedir

# Mail
mail = Mail()

# Login
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')

# DB
db = SQLAlchemy()
migrate = Migrate()

# Bootstrap
bootstrap = Bootstrap()

# Moment.js
moment = Moment()

# Babel
babel = Babel()


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


def create_app(config_class=Config):
    # App
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)
    app.es = Elasticsearch(hosts=[app.config['ES_URL']], 
                           basic_auth=(app.config['ES_LOGIN'], 
                                       app.config['ES_PASSWORD']),
                           ca_certs='http_ca.crt') \
        if app.config['ES_URL'] else None
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    # Blueprint
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
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

    return app

from app import models
