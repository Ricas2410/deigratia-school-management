"""
PythonAnywhere specific settings
This file contains settings optimized for PythonAnywhere deployment
"""

# Import base settings
from .ricas_school_manager.settings import *

# Override email settings for PythonAnywhere
# Free accounts don't support external SMTP, so we use console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For paid accounts, you can use:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Disable scheduler in production to avoid issues
RUN_SCHEDULER_IN_DEBUG = False

# Ensure static files are properly configured
STATIC_ROOT = '/home/deigratiams/deigratia-school-management/staticfiles'
MEDIA_ROOT = '/home/deigratiams/deigratia-school-management/media'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging configuration for PythonAnywhere
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/deigratiams/deigratia-school-management/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
