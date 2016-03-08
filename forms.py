from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class SignupForm(Form):
    username = StringField("username",validators=[DataRequired()])
    email = StringField("email",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])
    repeat_password = PasswordField("repeat password",validators=[DataRequired()])

class SigninForm(Form):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password",validators=[DataRequired()])

class MakeGroupForm(Form):
    groupname = StringField("groupname",validators=[DataRequired()])

class MakeEventForm(Form):
    eventname = StringField("eventname",validators=[DataRequired()])

class AddUserForm(Form):
    username = StringField("username",validators=[DataRequired()])
