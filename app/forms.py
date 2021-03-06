"""
forms.py
------------
Webpage forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash
from app.user import User
from flask_login import login_user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder":"Email Address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder":"Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name',  validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        results = mongo.db.Users.find_one({'email': self.email.data})
        print("IN VALIDATE")
        if results is None:
            #User isn't in DB, add user
            if self.password.data == self.password_confirm.data:
                hash = generate_password_hash(self.password.data)
                mongo.db.Users.insert({'email':self.email.data, 'password_hash': hash, 'first_name':self.first_name.data, 'last_name':self.last_name.data})
                result = mongo.db.Users.find_one({'email': self.email.data})
                user = User(self.first_name.data, self.last_name.data, self.email.data, result.get('_id'))
                login_user(user)
                return True
            else:
                return False #Passwords do not match
        else:
            return False     #Email already exists

class PandaForm(FlaskForm):
    meal_size = RadioField('Meal Size', validators=[DataRequired()], choices=['Bowl','Small Plate', 'Big Plate'])
    entrees = SelectField(u'Field name', choices = ['fake', 'rad'], validators = [DataRequired()])
    drink = StringField('Drink', validators=[DataRequired(), Email()])
    submit = SubmitField('Order')

class AccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name  = StringField('Last Name',  validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

class ResetPasswordRequestForm(FlaskForm):
    email  = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

    def validate_password(self, password):
        if self.password.data == self.password_confirm.data:
            self.hash = generate_password_hash(self.password.data)
        else:
            raise ValidationError('Mismatching passwords.')

class PaymentForm(FlaskForm):
    cardnumber = StringField('Card Number', validators=[DataRequired()])
    cardname = StringField('Name on Card',  validators=[DataRequired()])
    cardcode = StringField('CVC', validators=[DataRequired()])
    submit = SubmitField('Submit')

