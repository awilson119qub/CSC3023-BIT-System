from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
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
    @login_required
    def newsfeed():
        posts = Post.query.all()
        return render_template("newsfeed.html", user=current_user, posts=posts)
    
    # Discover/search route #
    @app.route('/search')
    @login_required
    def search():
        return render_template("search.html")
    
    # Discover to people route #
    @app.route('/people')
    @login_required
    def people():
        return render_template('people.html')

    # Discover to societies route #
    @app.route('/societies')
    @login_required
    def societies():
        return render_template('societies.html')

    # Discover to events route #
    @app.route('/events')
    @login_required
    def events():
        return render_template('events.html')

    # Discover to groups route #
    @app.route('/groups')
    @login_required
    def groups():
        return render_template('groups.html')

    # Message route #
    @app.route('/message')
    @login_required
    def message():
        return render_template("message.html")
    
    # Notification route #
    @app.route('/notification')
    @login_required
    def notification():
        return render_template("notification.html")
    
    # Profile route #
    @app.route('/profile')
    @login_required
    def profile():
        return render_template("profile.html", user=current_user)
    
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
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out')
        return redirect(url_for('login'))