from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from flask_login import UserMixin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # User Posts #
    posts = db.relationship('Post', backref='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '(User {})'.format(self.username)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_recommended = db.Column(db.Boolean, default=False)
    group_name = db.Column(db.String(100))

    def __repr__(self):
        return '(Post {})'.format(self.content)