from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_ckeditor import CKEditor
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

ckeditor = CKEditor(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_message = 'Чтобы войти на эту страницу, пожалуйста авторизуйтесь'
login.login_view = 'login'
bootstrap = Bootstrap(app)
moment = Moment(app)
	
	
from app import views, models, forms

'''if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Microblog startup')'''