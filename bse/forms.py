from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, email_validator


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')
    
    # username = StringField('Username', validators=[DataRequired()])
    # password = PasswordField('Password', validators=[
    #                          Length(min=6), DataRequired()])
    
