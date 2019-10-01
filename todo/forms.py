from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Regexp, Length, Email, EqualTo, ValidationError
from todo.models import User


class BookmarkForm(FlaskForm):
    url=URLField('Enter Url', validators=[DataRequired(), url()])
    description=StringField('description')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        
        if not self.description.data:
            self.description.data=self.url.data

        return True

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me Logged in')

class SignupForm(FlaskForm):
    username=StringField('Username', 
    validators=[DataRequired(), Length(3,80), Regexp('^[A-Za-z0-9_]{3,}$', 
    message='Username consists of numbers, letters, and underscores.')])

    password=PasswordField('Password',
    validators=[DataRequired(), EqualTo('password2', message='Password must match.')])

    password2=PasswordField('Confirm Password', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), (Length(1,120)), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('This email belongs to an existing User.')
    
    def validate_username(self,username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')


class RequestResetForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), (Length(1,120)), Email()])
    
    def validate_email(self, email_field):
        user = User.query.filter_by(email=email_field.data).first()
        if user is None:
            raise ValidationError('This email does not exist. Please register')
    
class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',
    validators=[DataRequired(), EqualTo('password2', message='Password must match.')])

    password2=PasswordField('Confirm Password', validators=[DataRequired()])


'''
class UpdateBookmarkForm(FlaskForm):
    url = URLField('Enter url', validators=[DataRequired(), url()])
    description = StringField('description')

    def validate_url(self, url):
        if url.data != current_user.url:
            user = User.query.filter_by()

            '''