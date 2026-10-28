import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env if present
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'civicpulse-ai-dev-secret-key-2026-secure-token')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'civicpulse.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(basedir, 'app', 'static', 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'pdf'}
    
    # Session and Security
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Escalation SLA Defaults (in hours)
    SLA_DAY2_HOURS = int(os.environ.get('SLA_DAY2_HOURS', 48))
    SLA_DAY4_HOURS = int(os.environ.get('SLA_DAY4_HOURS', 96))
    
    # AI Provider Settings
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'fallback') # 'gemini', 'openai', or 'fallback'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    
    # Notification & SMS/Email Simulation Settings
    SIMULATE_NOTIFICATIONS = os.environ.get('SIMULATE_NOTIFICATIONS', 'True').lower() in ('true', '1')
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Timezone
    TIMEZONE = 'Asia/Kolkata'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    # Use strict cookies in production
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
