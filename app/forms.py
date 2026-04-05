from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,RadioField
from wtforms.validators import DataRequired

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