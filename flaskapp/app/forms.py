from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SubmitField, IntegerField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class AuthForm(FlaskForm):
    username = StringField("Имя пользователя")
    pasw = PasswordField("Имя пользователя")
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повтори пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Неверное имя пользователя.')
        
class CreatePupilsForm(FlaskForm):
    count = IntegerField("Количество учеников")
    submit = SubmitField('Сгенерировать')

class CreateCodesForm(FlaskForm):
    submit_code = SubmitField('Сгенерировать коды')

class CreateTGIDForm(FlaskForm):
    tgid_input = StringField('TGID', validators=[DataRequired()])
    tg_hidden = HiddenField("TGhid")
    tgid_submit = SubmitField('Сохранить')