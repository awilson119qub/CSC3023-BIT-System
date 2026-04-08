from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm
from app.models import User, Post
from app import db

def register_routes(app):

    # Home route = Login/Register #
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    # Newsfeed route #
    @app.route('/newsfeed')
    def newsfeed():
        user = User.query.first()
        posts = Post.query.all()
        return render_template("newsfeed.html", user=user, posts=posts)
    
    # Discover/search route #
    @app.route('/search')
    def search():
        return render_template("search.html")
    
    # Message route #
    @app.route('/message')
    def message():
        return render_template("message.html")
    
    # Notification route #
    @app.route('/notification')
    def notification():
        return render_template("notification.html")
    
    # Profile route #
    @app.route('/profile')
    def profile():
        user = User.query.first()
        return render_template("profile.html", user=user)
    
    # Login route #
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('newsfeed'))
        
        form_type = request.args.get('form', 'login')

        # Register form #
        if form_type == 'register':
            form = RegistrationForm()
            if form.validate_on_submit():
                user = User(username=form.email.data, email=form.email.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('login', form='login'))
            return render_template("login.html", form=form, form_type='register')

        # Login form #
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password')
                return redirect(url_for('login', form='login'))

            login_user(user, remember=form.remember_me.data)
            flash('Login successful')
            return redirect(url_for('newsfeed'))

        return render_template("login.html", form=form, form_type='login')

    # Logout route #
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out')
        return redirect(url_for('login'))