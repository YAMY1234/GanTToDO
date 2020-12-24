# config.py=配置文件
import os
# 绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 先从环境变量中加载密钥，如果未设置则用默认密钥（极不安全）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cd499f96a0a4fc9853a0d67d2acb'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    UPLOAD_FOLDER = os.getcwd() + '/app/static//image/headpic/'  # 上传头像路径设置
    MAIL_SUBJECT_PREFIX = '[DDL Manager Team]'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    # MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USER') or 'Charles_Zhangz@163.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PWD') or 'OZSEZEOFQSHORZQZ'
    MAIL_SENDER = 'Gantt Admin<Charles_Zhangz@163.com>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # #############################################################################################
    # 括号里的四项分别是：
    # 用户名（不用改）、密码、主机（不用改）、schema名（要手动建了才能访问，有无table不要紧）
    # #############################################################################################
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        "mysql://%s:%s@%s:3306/%s?charset=utf8" \
        % ('root', 'lym20001221', '127.0.0.1', 'gantt')
    CREATE_DATABASE = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        "mysql://%s:%s@%s:3306/%s?charset=utf8" \
        % ('root', 'lym20001221', '127.0.0.1', 'gantt')
    CREATE_DATABASE = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        "mysql://%s:%s@%s:3306/%s?charset=utf8" \
        % ('root', 'lym20001221', '127.0.0.1', 'gantt')
    CREATE_DATABASE = False


config = {
    'development': DevelopmentConfig,  # 开发环境
    'testing': TestingConfig,  # 测试环境
    'production': ProductionConfig,  # 生产环境
    'default': DevelopmentConfig
}
