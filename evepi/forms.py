from flask.ext.wtf import Form
from wtforms import TextField, validators, PasswordField, SubmitField
from models import db, User


class SigninForm(Form):
    username = TextField("Username", [validators.Required("Please enter your username.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Sign In")
    uid = 0

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(username=self.username.data).first()

        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid username or password")
            return False


class SignupForm(Form):
    username = TextField("Username", [validators.Required("Please enter your username.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("That username is already taken")
            return False
        else:
            return True
