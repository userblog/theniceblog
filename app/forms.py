# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import fields, widgets
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import User
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
	username = StringField('Ваше имя', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	email = StringField('Электронная почта', validators=[DataRequired(message="Это поле обязательно для заполнения"), Email(message="Неверный email")])
	password = PasswordField('Пароль', validators=[DataRequired(message="Это поле обязательно для заполнения"), Length(min=8, message="Пароль должен содержать минимум 8 символов")])
	submit = SubmitField('Зарегистрироваться')
	
	def validate_username(self, username):
		user = User.query.filter_by(username=self.username.data).first()
		if user is True:
			raise ValidationError('Этот логин уже занят')
	
	def validate_email(self, email):
		email = User.query.filter_by(email=self.email.data).first()
		if email is True:
			raise ValidationError('Этот email уже занят')
	
class LoginForm(FlaskForm):
	email = StringField('Электронная почта', validators=[DataRequired(message="Это поле обязательно для заполнения"), Email(message="Неверный email")])
	password = PasswordField('Пароль', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	submit = SubmitField('Войти')

class PostForm(FlaskForm):
	header = StringField('Заголовок', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	text = CKEditorField('Текст', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	add_comment = BooleanField(' разрешить добовлять комментарии')
	submit = SubmitField('Опубликовать', default='True')

class EditPostForm(FlaskForm):
	header = StringField('Заголовок', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	text = TextAreaField('Текст', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	add_comment = BooleanField(' разрешить добовлять комментарии')
	submit = SubmitField('Изменить')

class CommentForm(FlaskForm):
	username = StringField('Ваше имя', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	text = TextAreaField('Текст', validators=[DataRequired(message="Это поле обязательно для заполнения")])
	post_id = HiddenField()
	submit = SubmitField('Добавить')
	
class SearchForm(FlaskForm):
	q = StringField()
	