from flask import render_template, flash
from app.forms import LoginForm
from app.models import User

def register_routes(app):
    @app.route('/')
    def newsfeed():
        user = User.query.first()

        posts = [
            {
                'author': {'username': 'Alysha'},
                'content': 'Who is attending the careers event tomorrow?',
                'time_ago': '2 hours ago',
                'likes': 3,
                'comments': 1,
                'shares': 0
            },
            {
                'author': {'username': 'Mark'},
                'content': 'Super happy to have achieved full marks in my exam!',
                'time_ago': '6 hours ago',
                'likes': 10,
                'comments': 3,
                'shares': 0
            },
            {
                'author': {'username': 'Jessica'},
                'content': 'I have lost my airpods outside the SU if anyone finds them please hand into reception',
                'time_ago': '7 hours ago',
                'likes': 7,
                'comments': 2,
                'shares': 5
            }
        ]
        
        return render_template("newsfeed.html",user = user, posts = posts)
    
    @app.route('/search')
    def search():
        return render_template("search.html")
    
    @app.route('/message')
    def message():
        return render_template("message.html")
    
    @app.route('/notification')
    def notification():
        return render_template("notification.html")
    
    @app.route('/profile')
    def profile():
        return render_template("profile.html")
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            flash ('Login requested for user {} with password {}' .format(form.username.data, form.password.data))
            
            print('form submitted')
        return render_template("login.html", form = form)