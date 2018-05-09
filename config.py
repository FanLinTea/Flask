

class Config:
    SECRET_KEY = 'wenchao1026'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USE_TLS = True
    MAIL_USERNAME = '15811280010@163.com'
    MAIL_PASSWORD = 'wangyang1026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[LuJiang]'
    FLASKY_MAIL_SENDER = 'LuJiang <Music>'

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/test_music'

class OutputConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = 'mysql://root:mysql@localhost:3306/music'

config = {
    'test':TestConfig,
    'output':OutputConfig
}