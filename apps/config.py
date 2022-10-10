import os


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = (os.getenv('DEBUG', 'False') == 'True')

    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
