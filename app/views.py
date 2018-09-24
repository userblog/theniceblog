from app import app, db
from flask import render_template, flash, redirect, url_for, request, abort
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, PostForm, CommentForm, SearchForm, EditPostForm
from flask_login import login_user, logout_user, current_user, login_required

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.chek_password(form.password.data):
			flash('Неверный логин или пароль')
			return redirect(url_for('login'))
		login_user(user)
		return redirect(url_for('add_post', _anchor='add_post'))
	return render_template('login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def reg():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		name = User.query.filter_by(username=form.username.data).first()
		email = User.query.filter_by(email=form.email.data).first()
		if name is not None:
			flash('Это имя уже занято')
			return redirect(url_for('reg'))
		elif email is not None:
			flash('Этот email уже занят')
			return redirect(url_for('reg'))
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('registration.html', form=form)

@login_required
@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def index():
	page = request.args.get('page', 1, type=int)
	per_page = app.config['POSTS_PER_PAGE']
	post = Post.query.order_by(Post.date.desc()).paginate(page, per_page, error_out=False)
	return render_template('indexx.html', post=post)
	
@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
	try:
		p = Post.query.filter_by(id=id).first()
		p.views += 1
		db.session.commit()
		comments = Comment.query.filter(Comment.post_id==p.id).order_by(Comment.date.desc()).all()
	except:
		abort(404)
	form = CommentForm()
	if current_user.is_authenticated:
		form.username.data = current_user.username

	if form.validate_on_submit():
		com = Comment(username=form.username.data, text=form.text.data, post_id=p.id)
		db.session.add(com)
		db.session.commit()
		return redirect(url_for('post', id=id, _anchor='comment-text'))
	return render_template('post.html', p=p, form=form, comments=comments)


@app.route('/add_post', methods=['GET','POST'])
@login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(header=form.header.data, text=form.text.data, user_id=current_user.id, add_comment=form.add_comment.data)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index', _anchor='post'))
	return render_template('add_post.html', form=form)

@app.route('/search', methods=['GET'])
def search():
	q = request.args.get('q')
	result = Post.query.filter(Post.header.contains(q) | Post.text.contains(q)).all()
	return render_template('search.html', result=result)
		
@app.route('/admin', methods=['GET'])
@login_required
def admin():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date.desc()).paginate(page, app.config['ADMIN_PER_PAGE'], error_out=False)
	comment_count = Comment.query.filter(Comment.post_id==Post.id).count()
	return render_template('admin.html', posts=posts, com_ct=comment_count)

@app.context_processor
def utility_processor():
    def comment_ct(id):
        return Comment.query.filter(Comment.post_id==id).count()
    return dict(comment_ct=comment_ct)


@app.route('/edit/post/<id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Post.query.get_or_404(id)
	form = EditPostForm()
	if form.validate_on_submit():
		post.header = form.header.data
		post.text = form.text.data
		post.add_comment=form.add_comment.data
		db.session.commit()
		flash('Изменения успешно сохранены')
		return redirect(url_for('edit_post', id=post.id, _anchor='edit_post'))
	form.add_comment.data = post.add_comment
	form.header.data = post.header
	form.text.data = post.text
	return render_template('edit_post.html', form=form, post=post)
		
@app.route('/post/<id>/delite')
@login_required
def delite(id):
	try:
		p = Post.query.filter_by(id=id).first()
		db.session.delete(p)
		db.session.commit()
	except:
		abort(404)
	return redirect(url_for('admin', _anchor='post'))
	
@app.route('/delite/comment/<id>')
@login_required
def del_comment(id):
	try:
		del_com = Comment.query.filter_by(id=id).first()
		db.session.delete(del_com)
		db.session.commit()
	except:
		abort(404)
	return redirect(url_for('post', id=del_com.post_id, _anchor='comment-text'))

			
			
			
		