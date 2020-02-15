from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileAllowed,FileField

from flask_login import current_user
from syblogpost.models import Users

class Login(FlaskForm):
    email   = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit  = SubmitField('Log in')

class Register(FlaskForm):
    email    = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password  = PasswordField('Password',validators=[DataRequired(),EqualTo('conpword', message = 'Password must match')])
    conpword  = PasswordField('Confirm Password',validators=[DataRequired()])
    submit    = SubmitField('Register')

    def check_email(self,field):
        if Users.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is already registered')

    def check_username(self,field):
        if Users.query.filter_by(username = field.data).first():
            raise ValidationError('Your Username is already registered')
    
class updateform(FlaskForm):
    email    = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    picture  = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit   = SubmitField('Update')

    def check_email(self,field):
        if Users.query.filter_by(email = field.data).first():
            raise ValidationError('Your email is already registered')

    def check_username(self,field):
        if Users.query.filter_by(username = field.data).first():
            raise ValidationError('Your Username is already registered')