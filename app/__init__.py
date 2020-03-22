from flask import Flask
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
loginManager = LoginManager(app)

from app import routes
from app.models import User

User.load(app)