import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Below code was added during Chapter 7
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # Can set a default SMTP server here. For testing purposes, run the test
    # server with "(venv) $ python -m smtpd -n -c DebuggingServer
    # localhost:8025" in a seperate command prompt window, then
    # "set MAIL_SERVER=localhost" and
    # "set MAIL_PORT=8025"

    # The MS_TRANSLATOR_KEY is the key for using the Microsoft's Translator
    # service free edition
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # Defaults to port 25 if the environment variable is not set
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USER_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # Do not enter username and password here as it will be saved to a
    # source file and distributed, exposing your password. Set your variables
    # in command line with $ set MAIL_PASSWORD='yourpassword' or find another
    # way of doing it.
    ADMINS = ['ryan.couper1@defence.gov.au',
              'ryan.couper@uon.edu.au',
              'socremi@hotmail.com'
              ]
    POSTS_PER_PAGE = 5
    LANGUAGES = ['en', 'es']  # Config for flask-babel (language translation)
    # To update the Babel file containing text to translate run:
    # (venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .
    # (venv) $ pybabel update -i messages.pot -d app/translations
    # Update the new additions to the various messages.po file with their
    # translations then run:
    # (venv) $ pybabel compile -d app/translations
