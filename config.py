#coding:utf8
import redis

class Config:
    SECRET_KEY = 'wenchao1026'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    MAIL_USERNAME = '15811280010@163.com'
    MAIL_PASSWORD = 'wangyang1026'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_MAIL_SUBJECT_PREFIX = '[LuJiang]'
    FLASKY_MAIL_SENDER = '15811280010@163.com'
    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    Music_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,db=1)
    # sessioin配置
    SESSION_TYPE = "redis"  # 指定session的保存位置
    SESSION_USE_SIGNER = True  # 设置sessioin存储签名
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 24 * 3600 * 2  # session的有效时间,单位秒

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/test_music'

class OutputConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = 'mysql://root:mysql@localhost:3306/music'

config = {
    'test':TestConfig,
    'output':OutputConfig
}