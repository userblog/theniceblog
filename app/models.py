from app import db, login, app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id): 
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True)
	email = db.Column(db.String(128))
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='user', lazy=True)
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)
		
	def chek_password(self, password):
		return check_password_hash(self.password_hash, password)
		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	header = db.Column(db.String(128), index=True)
	text = db.Column(db.String(512))
	date = db.Column(db.DateTime(), default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	comment_id = db.relationship('Comment', backref='post', lazy=True)
	add_comment = db.Column(db.Boolean)
	views = db.Column(db.Integer(), default=0)
	



class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(256))
	date = db.Column(db.DateTime(), default=datetime.utcnow)
	username = db.Column(db.String(32))
	edit_flag = db.Column(db.Boolean())
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	