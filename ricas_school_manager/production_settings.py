"""
Production settings for PythonAnywhere deployment
This file extends the base settings with production-specific configurations
"""

# Import all base settings
from .settings import *
import os

# Try to import decouple for environment variables
try:
    from decouple import config
except ImportError:
    # Fallback function if decouple is not available
    def config(key, default=None, cast=None):
        value = os.environ.get(key, default)
        if cast and value is not None:
            if cast == bool:
                return str(value).lower() in ('true', '1', 'yes', 'on')
            elif cast == int:
                return int(value)
            elif callable(cast):
                return cast(value)
        return value

# Override settings for production
DEBUG = config('DEBUG', default=False, cast=bool)

# Security settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# Allowed hosts
ALLOWED_HOSTS_STR = config('ALLOWED_HOSTS', default='localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',') if host.strip()]

# Add WhiteNoise middleware for static files in production
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Static files configuration for production
STATIC_ROOT = '/home/deigratiams/deigratia-school-management/staticfiles'
MEDIA_ROOT = '/home/deigratiams/deigratia-school-management/media'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email settings for production
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Set DEFAULT_FROM_EMAIL safely
_default_from_email = config('DEFAULT_FROM_EMAIL', default='')
if not _default_from_email and EMAIL_HOST_USER:
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
elif _default_from_email:
    DEFAULT_FROM_EMAIL = _default_from_email
else:
    DEFAULT_FROM_EMAIL = 'admin@localhost'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
    SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

# Disable scheduler in production to avoid issues
RUN_SCHEDULER_IN_DEBUG = False

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/deigratiams/deigratia-school-management/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'backup': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Database configuration (can be overridden with environment variables)
DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
# Otherwise, use the default SQLite configuration from base settings
