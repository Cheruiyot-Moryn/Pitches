import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moureen:12345@localhost/pitches'
    SECRET_KEY ='qwerty'
    MAIL_SERVER ='smtp.googlemail.com'
    MAIL_PORT =587
    MAIL_USE_TLS =True
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    
    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI='postgresql://pqdatncnedjjkp:c53b3fd55395fe7bff7b40f6ca749e1c44bd570d8132ce2b9b9b76a131c738ff@ec2-52-200-215-149.compute-1.amazonaws.com:5432/darsjivh3me8bu'
    SECRET_KEY = 'qwerty'
    pass

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://moureen:12345@localhost/pitches_test'


class DevConfig(Config):
    DEBUG = True

config_options= {
    'development':DevConfig,
    'production':ProdConfig,
    'test':TestConfig
}