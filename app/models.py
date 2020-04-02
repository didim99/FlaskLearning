from flask_login import UserMixin
from app import loginManager
from vkapi import VKAPI
import hashlib
import json
import os


class User(UserMixin):
    KEY_LOGIN = 'login'
    KEY_PASSW = 'passw'

    userList = None

    login = ''
    passw = ''
    is_external = False

    def __init__(self, data):
        if User.KEY_LOGIN in data:
            self.login = data[User.KEY_LOGIN]
            self.passw = data[User.KEY_PASSW]
        else:
            self.is_external = True
            self.login = data[VKAPI.KEY_ID]
            self.passw = data[VKAPI.KEY_TOKEN]
            if self.login not in User.userList:
                User.userList[self.login] = self
            self.api = VKAPI(self)
            self.info = self.api.method('users.get', {'fields': "photo_50"})
            self.info = self.info[0]

    def get_id(self):
        return self.login

    def get_full_name(self):
        try:
            return self.info['first_name'] + ' ' + self.info['last_name']
        except AttributeError:
            return self.login

    def avatar_url(self):
        try:
            return self.info['photo_50']
        except AttributeError:
            return ''

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
