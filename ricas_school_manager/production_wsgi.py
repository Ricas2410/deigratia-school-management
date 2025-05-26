"""
WSGI config for ricas_school_manager project in production.

This file is specifically for PythonAnywhere deployment.
It uses the production settings which include environment variable support.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/deigratiams/deigratia-school-management'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module to use production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricas_school_manager.production_settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
