import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    VKAPI = {
        'v': '5.122',
        'client_id': '7386546',
        'redirect_uri': 'https://didim.eclabs.ru/other/tstu/vkapi/verify.php',
        'state': os.environ.get('VKAPI_STATE') or 'you-will-never-guess',
        'response_type': 'code'
    }
