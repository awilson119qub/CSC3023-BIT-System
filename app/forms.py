from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from flask_login import current_user
class RegistrationForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long.')])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords do not match.')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already exists. Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    content = TextAreaField(
        'What’s on your mind?',
        validators=[
            DataRequired(message='Text must be entered to post.'),
            Length(max=1000, message='Post must be less than 1000 characters.')])
    submit = SubmitField('Post')

class ProfileForm(FlaskForm):
    username = StringField('Full Name', validators=[DataRequired(), Length(max=64)])
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    course = StringField('Course', validators=[Length(max=120)])
    year_of_study = StringField('Year of Study', validators=[Length(max=50)])
    accommodation = StringField('Accommodation', validators=[Length(max=120)])
    hometown = StringField('Hometown', validators=[Length(max=120)])
    interests = StringField('Interests', validators=[Length(max=255)])
    submit = SubmitField('Save Changes')