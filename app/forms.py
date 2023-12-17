from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class AuthForm(FlaskForm):
    username = StringField("Имя пользователя")
    pasw = PasswordField("Имя пользователя")
    submit = SubmitField('Войти')