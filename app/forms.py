from flask_wtf import FlaskForm
from sqlalchemy import Boolean
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo


class OrderForm(FlaskForm):
    car_id = IntegerField('Car ID', validators=[DataRequired()])
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_age = IntegerField('Customer Age', validators=[DataRequired(), NumberRange(min=18, message="You must be at least 18 years old to rent a car.")])
    customer_email = StringField('Customer Email', validators=[DataRequired(), Email()])
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Place Order')


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class RegistrationFrom(FlaskForm):
    name = StringField('Full Name: ', validators=[DataRequired()])
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password: ', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField()
