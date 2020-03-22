from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange


ATTR_ACTION = 'action'
ATTR_MANAGER = 'manager'
ATTR_KEY_LEN = 'length'
ATTR_KEY_E = 'keyE'
ATTR_KEY_D = 'keyD'
ATTR_KEY_N = 'keyN'
ACTION_GEN_KEY = 'gen_key'
ACTION_SET_KEY = 'set_key'
ACTION_GO = 'go'


class AuthForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    passw = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class KeyGenForm(FlaskForm):
    action = HiddenField(default=ACTION_GEN_KEY)
    length = IntegerField('Длина ключа', validators=[DataRequired()])
    submit = SubmitField('Сгенерировать')


class KeySetForm(FlaskForm):
    action = HiddenField(default=ACTION_SET_KEY)
    keyE = IntegerField('E', validators=[DataRequired(), NumberRange()])
    keyD = IntegerField('D', validators=[DataRequired(), NumberRange()])
    keyN = IntegerField('N', validators=[DataRequired(), NumberRange()])
    submit = SubmitField('Установить')
