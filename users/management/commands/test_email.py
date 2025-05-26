from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Test email configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
            required=True
        )

    def handle(self, *args, **options):
        recipient_email = options['to']
        
        self.stdout.write(self.style.SUCCESS('Testing email configuration...'))
        
        # Display current email settings (without password)
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        
        try:
            # Send test email
            subject = 'Test Email from Deigratia School Management System'
            message = '''
This is a test email to verify that your email configuration is working correctly.

If you receive this email, your email settings are properly configured!

Best regards,
School Management System
            '''
            
            result = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False
            )
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Test email sent successfully to {recipient_email}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send test email to {recipient_email}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error sending test email: {str(e)}')
            )
            
            # Provide troubleshooting tips
            self.stdout.write('\n🔧 Troubleshooting tips:')
            self.stdout.write('1. Check your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env')
            self.stdout.write('2. For Gmail, use an App Password (not your regular password)')
            self.stdout.write('3. Ensure 2-Step Verification is enabled on your Google account')
            self.stdout.write('4. Generate App Password: https://myaccount.google.com/apppasswords')
            self.stdout.write('5. Check your internet connection')
            
            if 'Network is unreachable' in str(e):
                self.stdout.write('\n🌐 Network Error:')
                self.stdout.write('- This might be a temporary network issue')
                self.stdout.write('- Try again in a few minutes')
                self.stdout.write('- Check if PythonAnywhere is experiencing issues')
            
            if 'Authentication failed' in str(e):
                self.stdout.write('\n🔐 Authentication Error:')
                self.stdout.write('- Double-check your EMAIL_HOST_USER (full email address)')
                self.stdout.write('- Verify your EMAIL_HOST_PASSWORD (16-character app password)')
                self.stdout.write('- Make sure 2-Step Verification is enabled on Google account')
