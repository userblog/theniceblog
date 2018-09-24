import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = '4#@$-()?!/09876544*^¥€¢£~π÷×¶∆}][✓™®©%¥^°€¢'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	MAIL_SERVER = 'smtp.yandex.ru'
	MAIL_PORT = 587
	MAIL_USE_TLS = 1
	MAIL_USERNAME = 'imslavik@yandex.ru'
	MAIL_PASSWORD = 'rusins1l0a0v1i1k995'
	ADMINS = ['imslavik@yandex.ru']
    
	POSTS_PER_PAGE = 2
	ADMIN_PER_PAGE = 2
	
	
    