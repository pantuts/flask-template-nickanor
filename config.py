import os
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    # Analytics
    GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')
    SEGMENT_API_KEY = os.environ.get('SEGMENT_API_KEY', '')

    REDIS_URL = os.getenv('REDISTOGO_URL', 'http://localhost:6379')
    urllib.parse.uses_netloc.append('redis')
    url = urllib.parse.urlparse(REDIS_URL)
    RQ_DEFAULT_HOST = url.hostname
    RQ_DEFAULT_PORT = url.port
    RQ_DEFAULT_PASSWORD = url.password
    RQ_DEFAULT_DB = 0

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    DEBUG = False
    USE_RELOADER = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'data.sqlite'))
    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
