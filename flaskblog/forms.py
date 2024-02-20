from collections.abc import Sequence
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class Registration_form(FlaskForm):
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


class Login_form(FlaskForm):
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log in')