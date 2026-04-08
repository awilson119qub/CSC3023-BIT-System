from flask import Flask
from config import DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)
    login.login_view = 'login'

    from app.models import User

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from app.routes import register_routes
    register_routes(app)

    return app
