from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class AuthForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
