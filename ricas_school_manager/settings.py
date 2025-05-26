"""
Django settings for ricas_school_manager project.
This file integrates settings from both the DGMS website and School Management System.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-integration-key-replace-in-production'
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party apps
    'crispy_forms',
    'crispy_bootstrap4',
    'mathfilters',
    'widget_tweaks',
    'tinymce',

    # Website (DGMS) app
    'website',

    # SMS apps
    'users',
    'courses',
    'assignments',
    'attendance',
    'communications',
    'dashboard',
    'fees',
    'payroll',
    'appointments',  # Appointment booking system
    'backup',  # Backup and restore system
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ricas_school_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.site_settings',
                'dashboard.context_processors.sidebar_context',
                'dashboard.context_processors.user_preferences',
                'dashboard.context_processors.notifications_context',
                'appointments.context_processors.appointment_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ricas_school_manager.wsgi.application'


# Database - SINGLE DATABASE FOR BOTH SYSTEMS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Default system name
DEFAULT_SCHOOL_NAME = 'Ricas School Manager'

# Use custom user model from SMS
AUTH_USER_MODEL = 'users.CustomUser'

# Authentication settings
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'website:home'

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'users.auth_backends.FlexibleStudentBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Password reset settings
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour
PASSWORD_RESET_DONE_REDIRECT_URL = 'users:password_reset_done'
PASSWORD_RESET_CONFIRM_TEMPLATE_NAME = 'users/password_reset_confirm.html'

# TinyMCE Configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': '100%',
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
        textcolor save link image media preview codesample contextmenu
        table code lists fullscreen insertdatetime nonbreaking
        contextmenu directionality searchreplace wordcount visualblocks
        visualchars code fullscreen autolink lists charmap print hr
        anchor pagebreak
        ''',
    'toolbar1': '''
        fullscreen preview bold italic underline | fontselect,
        fontsizeselect | forecolor backcolor | alignleft alignright |
        aligncenter alignjustify | indent outdent | bullist numlist table |
        | link image media | codesample |
        ''',
    'toolbar2': '''
        visualblocks visualchars |
        charmap hr pagebreak nonbreaking anchor | code |
        ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# Academic years and terms (from SMS)
from datetime import datetime
CURRENT_YEAR = datetime.now().year
ACADEMIC_YEARS = [str(year) for year in range(CURRENT_YEAR - 1, CURRENT_YEAR + 5)]
ACADEMIC_TERMS = ["First Term", "Second Term", "Third Term"]

# Email settings - Uses custom backend that gets settings from SchoolSettings model
EMAIL_BACKEND = 'users.backends.SchoolEmailBackend'
ALTERNATIVE_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Default fallback settings (will be overridden by SchoolSettings)
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'skillnetservices@gmail.com'
DEFAULT_FROM_EMAIL = 'skillnetservices@gmail.com'

# Try to import local settings if they exist
try:
    from .local_settings import *
except ImportError:
    pass

# Scheduler settings
RUN_SCHEDULER_IN_DEBUG = True  # Set to False to disable scheduler in debug mode
