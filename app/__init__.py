from flask import Flask
from app.extensions import db, migrate, mail, login_manager
from app.api import init_api


login_manager.login_view = 'users.login'
login_manager.login_message = "Please login to access this page"


def create_app(config='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    init_api(app)

    from app.views.cars import cars_bp
    from app.views.orders import orders_bp
    from app.views.users import users_bp

    app.register_blueprint(cars_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(users_bp)

    return app
