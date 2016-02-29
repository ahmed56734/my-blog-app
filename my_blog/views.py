from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import desc
from my_blog import app, db, login_manager
from forms import LoginForm, SignupForm, PostForm
from models import User, Post


import re
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/home')
def home():
	if current_user.is_authenticated:
	    return redirect('/'+current_user.username)
	flash('You mush login first')
	return redirect(url_for('login'))


@app.route('/<username>')
def user(username):
	user_id = User.query.filter_by(username=username).first_or_404().id
	posts = Post.query.filter_by(user_id=user_id).order_by(desc(Post.date)).all()
	if len(posts) == 0:
		nothing = True
	else:
		nothing = False
	return render_template('user.html', posts=posts, nothing=nothing, activehome='active')

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect('/')
	form = LoginForm()
	if request.method == "GET":
		return render_template('login.html',form=form, activelogin='active')
	else:
		if form.validate_on_submit():
			user = User.query.filter_by(username=form.username.data).first()
			if user is not None and user.check_password(form.password.data):
				login_user(user, form.remember_me.data)
				return redirect('/'+user.username)
			else:	
				flash('Incorrect username or password.')

		return render_template("login.html", form=form, activelogin='active')

@app.route("/signup", methods=["GET", "POST"])
def signup():
	if current_user.is_authenticated:
		return redirect('/')
	form = SignupForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,password = form.password.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		flash('Welcome, {}!'.format(user.username))
		return redirect('/'+user.username)
	return render_template("signup.html", form=form, activesignup='active')

@app.route("/logout")
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('login'))

@app.route("/newpost", methods=["GET", "POST"])
@login_required
def newpost():
	form = PostForm()
	if form.validate_on_submit():
		title = form.title.data
		content = form.content.data
		post = Post(user=current_user, title=title, content=content)
		db.session.add(post)
		db.session.commit()
		flash("New post added")
		return redirect('/'+current_user.username)
	return render_template('newpost.html', form=form, activeadd="active")


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s<br>' % p.replace('\n', '<br>\n') \
        for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result