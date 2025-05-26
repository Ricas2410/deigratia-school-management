from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check production settings configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking Production Configuration...'))
        
        # Check if we're using production settings
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set')
        self.stdout.write(f"Settings Module: {settings_module}")
        
        # Check DEBUG status
        debug_status = "🟢 Production" if not settings.DEBUG else "🟡 Development"
        self.stdout.write(f"DEBUG: {settings.DEBUG} ({debug_status})")
        
        # Check ALLOWED_HOSTS
        self.stdout.write(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        # Check SECRET_KEY
        if settings.SECRET_KEY.startswith('django-insecure-'):
            self.stdout.write(self.style.WARNING("⚠️  SECRET_KEY appears to be default/insecure"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ SECRET_KEY appears to be customized"))
        
        # Check static files
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
        
        # Check middleware
        has_whitenoise = 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE
        whitenoise_status = "✅ Enabled" if has_whitenoise else "❌ Not found"
        self.stdout.write(f"WhiteNoise Middleware: {whitenoise_status}")
        
        # Check email settings
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        # Check database
        db_engine = settings.DATABASES['default']['ENGINE']
        db_name = settings.DATABASES['default']['NAME']
        self.stdout.write(f"Database: {db_engine}")
        self.stdout.write(f"Database Name: {db_name}")
        
        # Security checks for production
        if not settings.DEBUG:
            self.stdout.write(self.style.SUCCESS('\n🔒 Production Security Checks:'))
            
            security_settings = [
                ('SECURE_SSL_REDIRECT', getattr(settings, 'SECURE_SSL_REDIRECT', False)),
                ('SECURE_HSTS_SECONDS', getattr(settings, 'SECURE_HSTS_SECONDS', 0)),
                ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', False)),
                ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', False)),
            ]
            
            for setting_name, setting_value in security_settings:
                status = "✅" if setting_value else "❌"
                self.stdout.write(f"{status} {setting_name}: {setting_value}")
        
        self.stdout.write(self.style.SUCCESS('\n✅ Configuration check completed!'))
