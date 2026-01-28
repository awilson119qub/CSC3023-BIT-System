from flask import render_template

def register_routes(app):
    @app.route('/')
    def index():
        return render_template("newsfeed.html")
    
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