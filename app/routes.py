from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, PostForm, ProfileForm
from app.models import User, Post
from app import db
from datetime import datetime, timezone, timedelta

# CHATGPT USED PROMPT = Can you give me a python function that returns the date/time a post was posted to a category such as "Just Now", "1 day ago", etc #
def time_ago(post_time):
    now = datetime.now(timezone.utc)

    if post_time.tzinfo is None:
        post_time = post_time.replace(tzinfo=timezone.utc)

    diff = now - post_time
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} min ago" if minutes == 1 else f"{minutes} mins ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"
    elif seconds < 604800:
        days = seconds // 86400
        return f"{days} day ago" if days == 1 else f"{days} days ago"
    else:
        weeks = seconds // 604800
        return f"{weeks} week ago" if weeks == 1 else f"{weeks} weeks ago"

def register_routes(app):

    # Home route = Login/Register #
    @app.route('/')
    def home():
        return redirect(url_for('login'))

    # Newsfeed route #
    @app.route('/newsfeed', methods=['GET', 'POST'])
    @login_required
    def newsfeed():
        form = PostForm()

        if form.validate_on_submit():
            post = Post(content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Posted!')
            return redirect(url_for('newsfeed'))

        selected_filter = request.args.get('filter', 'newest')
        filtered_posts = Post.query

        # Time filter #
        if selected_filter == 'today':
            since = datetime.now(timezone.utc) - timedelta(days=1)
            filtered_posts = filtered_posts.filter(Post.timestamp >= since)

        elif selected_filter == '3days':
            since = datetime.now(timezone.utc) - timedelta(days=3)
            filtered_posts = filtered_posts.filter(Post.timestamp >= since)

        elif selected_filter == 'week':
            since = datetime.now(timezone.utc) - timedelta(days=7)
            filtered_posts = filtered_posts.filter(Post.timestamp >= since)

        elif selected_filter == 'month':
            since = datetime.now(timezone.utc) - timedelta(days=30)
            filtered_posts = filtered_posts.filter(Post.timestamp >= since)

        # Always show newest posts first #
        filtered_posts = filtered_posts.order_by(Post.timestamp.desc())

        posts = filtered_posts.all()

        return render_template("newsfeed.html", user=current_user, posts=posts, form=form, selected_filter=selected_filter, time_ago=time_ago)
    
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
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        form = ProfileForm()
        edit_mode = request.args.get('edit') == 'true'

        if request.method == 'GET':
            form.username.data = current_user.username
            form.bio.data = current_user.bio
            form.course.data = current_user.course
            form.year_of_study.data = current_user.year_of_study
            form.accommodation.data = current_user.accommodation
            form.hometown.data = current_user.hometown
            form.interests.data = current_user.interests

        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.bio = form.bio.data
            current_user.course = form.course.data
            current_user.year_of_study = form.year_of_study.data
            current_user.accommodation = form.accommodation.data
            current_user.hometown = form.hometown.data
            current_user.interests = form.interests.data

            db.session.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('profile'))

        return render_template("profile.html", user=current_user, form=form, edit_mode=edit_mode)

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
                user = User(username=form.username.data, email=form.email.data)
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