import os
from datetime import timedelta

class Config:
    # Secret key for securely signing session cookies and CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")
    
    # SQLite database path (can be swapped with environment variable for production)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///device_monitoring.db")
    
    # Disable track modifications to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key")  # Secure key for JWT encoding
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)  # Token validity duration
