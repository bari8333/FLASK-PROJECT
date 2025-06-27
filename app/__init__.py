from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from .utils import setup_logging

# Extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # JWT Config (Cookies-based)
    app.config.update({
        "JWT_TOKEN_LOCATION": ["cookies"],
        "JWT_COOKIE_SECURE": False,  # Set to True in production with HTTPS
        "JWT_ACCESS_COOKIE_PATH": "/",
        "JWT_REFRESH_COOKIE_PATH": "/token/refresh",
        "JWT_COOKIE_CSRF_PROTECT": False
    })

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Setup logging
    setup_logging(app)

    # JWT Error Handlers
    @jwt.unauthorized_loader
    def custom_unauthorized_response(callback):
        flash("Please log in to continue.", "warning")
        return redirect(url_for('auth.login'))

    @jwt.invalid_token_loader
    def custom_invalid_token_response(callback):
        flash("Invalid or expired token. Please log in again.", "warning")
        return redirect(url_for('auth.login'))

    @jwt.expired_token_loader
    def custom_expired_token_response(jwt_header, jwt_payload):
        flash("Your session has expired. Please log in again.", "warning")
        return redirect(url_for('auth.login'))

    @jwt.revoked_token_loader
    def custom_revoked_token_response(jwt_header, jwt_payload):
        flash("Token has been revoked. Please log in again.", "warning")
        return redirect(url_for('auth.login'))

    # Blueprint Registration
    with app.app_context():
        from .routes.auth import auth_bp
        from .routes.device import device_bp
        from .routes.diagnostics import diagnostics_bp
        from .routes.main import main_bp

        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(device_bp, url_prefix="/devices")
        app.register_blueprint(diagnostics_bp, url_prefix="/diagnostics")
        app.register_blueprint(main_bp)

        # Create tables (safe if already exist)
        db.create_all()

    return app
