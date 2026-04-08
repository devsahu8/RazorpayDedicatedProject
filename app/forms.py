from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,RadioField,IntegerField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError
from app.models import User
import sqlalchemy as sa
from app import db


class IndexForm(FlaskForm):
    choice=RadioField("Choose your Next Step",choices=[
        ("option1","Check the status of orders I sended."),
        ("option2","Check the status of orders I recived."),
        ("option3","Create a order and send it to a another user.")
    ],validators=[DataRequired()])
    submit=SubmitField("Submit")

class LoginForm(FlaskForm):
    username=StringField("Enter your username.",validators=[DataRequired()])
    password=PasswordField("Enter your password.",validators=[DataRequired()])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("submit")

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class option3Form(FlaskForm):
    senderName=StringField("Enter the username where you want to send Order Recipt.",validators=[DataRequired()])
    reciptAmount=IntegerField("Enter amount",validators=[DataRequired()])
    submit=SubmitField("submit")

class option2Form(FlaskForm):
    submit=SubmitField("Pay all orders.")