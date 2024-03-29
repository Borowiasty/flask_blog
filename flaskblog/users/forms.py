from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), 
                                                    Length(min= 2, max= 20)])
    
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('User with that username allready exist')
        
    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('User with that email allready exist')


class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), 
                                                    Length(min= 2, max= 20)])
    
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    picture = FileField('Update profile picture', validators= [FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('User with that username allready exist')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('User with that email allready exist')
            
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    submit = SubmitField("Request password reset")

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Reset password")