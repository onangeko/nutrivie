import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        conn = sqlite3.connect('Nutrivie')
        curs = conn.cursor()
        curs.execute("SELECT email FROM login where email = (?)", [email.data])
        valemail = curs.fetchone()
        if valemail is None:
            raise ValidationError('This Email ID is not registered. Please register before login')


class RegistrationForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')


class ProfileForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    height = IntegerField('Height', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    seggs = RadioField('Sexe Biologique', choices=[
        (1, 'M'), (2, 'F')],
                       default=1, coerce=int)
    submit = SubmitField('OK')
