import os
from dotenv import load_dotenv

load_dotenv()


def normalize_database_url(url):
    if not url:
        return url
    # Render PostgreSQL URLs are supported directly. This also keeps
    # compatibility with providers that still return postgres:// URLs.
    if url.startswith('postgres://'):
        return url.replace('postgres://', 'postgresql://', 1)
    return url


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'calorify-dev-secret-key-change-in-prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 280,
    }
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    FRONTEND_ORIGINS = [
        origin.strip().rstrip('/')
        for origin in os.getenv(
            'FRONTEND_ORIGIN',
            'http://localhost:5173,http://localhost:3000'
        ).split(',')
        if origin.strip()
    ]


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.getenv('DATABASE_URL', 'sqlite:///calorify_dev.db')
    )


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv('DATABASE_URL'))


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
