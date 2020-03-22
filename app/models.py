from flask_login import UserMixin
from app import loginManager
import hashlib
import json
import os


class User(UserMixin):
    userList = None
    login = ''
    passw = ''

    def __init__(self, data):
        self.login = data['login']
        self.passw = data['passw']

    def get_id(self):
        return self.login

    def check_password(self, password):
        return hashlib.md5(password.encode('utf-8')).hexdigest() == self.passw

    def __repr__(self):
        return F'User: {self.login}'

    @staticmethod
    @loginManager.user_loader
    def load_user(_login):
        if _login not in User.userList:
            return None
        else:
            return User.userList[_login]

    @staticmethod
    def load(_context):
        if not User.userList:
            filename = os.path.join(_context.root_path, 'data', 'userdata.json')
            file = open(filename, 'r')
            data = json.load(file)
            file.close()

            User.userList = {}
            for item in data:
                User.userList[item['login']] = User(item)
