import logging  # added in chapter 7
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler  # Added in ch7
import os  # Added in chapter 7
from flask_mail import Mail  # This line was added in Chapter 10
from flask_bootstrap import Bootstrap  # Added in Ch11
from flask_moment import Moment  # Ch12
from flask_babel import Babel, lazy_gettext as _l  # Ch13
from flask import request  # Ch13

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# The next few lines were added in Chapter 13 for multilanguage support
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
# End Chapter 13 code
mail = Mail(app)  # This line was added in chapter 10
#  login.login_view = 'login'  # Omitted in Chapter 13
bootstrap = Bootstrap(app)  # Ch11
moment = Moment(app)  # Ch12
babel = Babel(app)  # Ch13


# The code below this line was added in Chapter 7
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # The following code is related to logging minor errors to a file
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log',
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


# Method added in Chapter 13 - relates to language translation.
@babel.localeselector
def get_local():
    return request.accept_languages.best_match(app.config['LANGUAGES'])


from app import routes, models
from app import errors  # Added in chapter 7
