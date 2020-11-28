from flask_wtf import FlaskForm # conditional that validates user in form submission
from flask_wtf.file import FileField, FileAllowed # conditional that validates user in form submission
from flask_login import current_user  # We only want files with a . in the filename
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, TextField # conditional that validates user in form submission
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # conditional that validates user in form submission
from docst.models import User # conditional that validates user in form submission

class RegistrationForm(FlaskForm):  # registration form function
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    #Custom validation for Username and Email to ensure no duplicate users are allready in database
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #retrieves first value
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #retrieves first value
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class ContactForm(FlaskForm): # contact form function
  name = TextField("Name", validators=[DataRequired("Please enter your name.")])
  email = TextField("Email",  validators=[DataRequired("Please enter your Email.")])
  subject = TextField("Subject",  validators=[DataRequired("Please enter a subject.")])
  message = TextAreaField("Message",  validators=[DataRequired("Please enter a message.")]) 
  submit = SubmitField('Send')

class LoginForm(FlaskForm): # login form function
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm): # update account function
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username): # validates username
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email): # validates email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

                
                
                
class PostForm(FlaskForm): # post function
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')