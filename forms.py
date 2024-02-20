from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Registration_form(FlaskForm):
    username = StringField('Username', validators= [DataRequired(), 
                                                    Length(min= 2, max= 20)])
    
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


class Login_form(FlaskForm):
    email = StringField('Email', validators= [DataRequired(),
                                              Email(),])
    
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log in')