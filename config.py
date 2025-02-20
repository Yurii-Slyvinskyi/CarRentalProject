import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### setting Flask-Mail #####
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'testmail.carrental@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'tkck cceb rcqx xjyz'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'A SECRET KEY FOR DEVELOPMENT'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
                                            'postgresql://postgres:12345@localhost/car_rental_db'


class TestingConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'A SECRET KEY FOR TESTING'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
                                            'postgresql://postgres:12345@localhost/test_car_rental_db'


class ProductionConfig(BaseConfig):
    DEBUG = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                                            'postgresql://postgres:12345@localhost/car_rental_db'

    @staticmethod
    def init_app(app):
        if not ProductionConfig.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in environment variables")
        if not ProductionConfig.SQLALCHEMY_DATABASE_URI:
            raise ValueError("PRODUCTION_DATABASE_URI is not set in environment variables")