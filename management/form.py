from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField ,PasswordField ,SubmitField , TextAreaField
from wtforms.validators import DataRequired , Length , EqualTo , ValidationError
from management.datbase import *



class signupform(FlaskForm):
    username = StringField('Username :' , validators=[DataRequired() , Length(max=50)])
    email = StringField('Email :',validators=[DataRequired() ])
    bio = StringField('Bio :',validators=[DataRequired() ])
    password = PasswordField('Password :' , validators=[DataRequired() , Length(min=8 ,max=15)])
    cnfpass = PasswordField('Confirm Password' , validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    

    def validate_email(self , email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('The email is already been Used, Pleace Choose Different Email or login With the Email')


class loginform(FlaskForm):
    email = StringField('Email :',validators=[DataRequired()])
    password = PasswordField('Password :' , validators=[DataRequired() , Length(min=8 ,max=15)])
    
    submit = SubmitField('Login')




class Accountform(FlaskForm):
    username = StringField('Username :' , validators=[DataRequired() , Length(min = 4, max=10)])
    email = StringField('Email :',validators=[DataRequired()])
    picture = FileField('Update Profile Picture')
    bio = StringField('Bio :' ,validators=[DataRequired()] )
    submit = SubmitField('Update')
    

    def validate_email(self , email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('The email is already been Used, Pleace Choose Different Email or login With the Email')


class postform(FlaskForm):
    title =  StringField('Title :' ,validators=[DataRequired()] )
    post_data = TextAreaField('Post :' , validators=[DataRequired()])
    submit = SubmitField('Submit')
