import json
from requests import post
from app import app


class VKAPI(object):
    API_URL = 'https://api.vk.com/method/'
    KEY_V = 'v'
    KEY_ID = 'user_id'
    KEY_TOKEN = 'access_token'
    KEY_RESPONSE = 'response'
    KEY_ERROR = 'error'
    KEY_ERR_DESC = 'error_description'

    def __init__(self, user):
        self.v = app.config['VKAPI'][VKAPI.KEY_V]
        self.access_token = user.passw
        self.user_id = user.login

    def method(self, name, params=None):
        if params is None:
            params = {}
        params[VKAPI.KEY_TOKEN] = self.access_token
        params[VKAPI.KEY_V] = self.v
        r = post(VKAPI.API_URL + name, data=params)
        data = json.loads(r.text)
        if VKAPI.KEY_ERROR in data:
            error = data[VKAPI.KEY_ERROR]
            raise IOError(error['error_code'] + ': ' + error['error_msg'])
        return data[VKAPI.KEY_RESPONSE]
