from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
loginManager = LoginManager(app)

from app import routes
from app.models import User
from app.forms import ATTR_KEY_LEN
from encryption.rsa import RSAKey

app.jinja_env.globals.update(get_key_lengths=RSAKey.get_possible_len)
app.jinja_env.globals.update(ATTR_KEY_LEN=ATTR_KEY_LEN)

User.load(app)
