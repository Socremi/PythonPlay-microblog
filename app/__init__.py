from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# The next line tells Flask-Login what view function handles logging in (the
# name used in a url_for() call). Used when a user attempts to access a page
# that requires the user to be logged in.
login.login_view = 'login'

from app import routes, models
