from flask import Flask
from config import Config
from .extensions import db, bcrypt, login_manager, mail, admin, limiter
from .error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        from .routes import auth, main
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)

        db.create_all()

    # Register error handlers
    register_error_handlers(app)

    return app
