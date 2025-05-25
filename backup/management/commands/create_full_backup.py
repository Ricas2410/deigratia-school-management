import os
import json
import zipfile
import shutil
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import connection
from django.apps import apps
import tempfile

class Command(BaseCommand):
    help = 'Create a comprehensive backup of all school data including database, media files, and settings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='backups',
            help='Directory to store backup files (default: backups)'
        )
        parser.add_argument(
            '--include-media',
            action='store_true',
            default=True,
            help='Include media files in backup (default: True)'
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            default=True,
            help='Compress backup files (default: True)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting comprehensive school data backup...'))
        
        # Create backup directory
        backup_dir = Path(options['output_dir'])
        backup_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'school_backup_{timestamp}'
        
        # Create temporary directory for backup files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            backup_path = temp_path / backup_name
            backup_path.mkdir()
            
            try:
                # 1. Create database backup
                self.stdout.write('📊 Creating database backup...')
                self.create_database_backup(backup_path)
                
                # 2. Backup media files
                if options['include_media']:
                    self.stdout.write('📁 Backing up media files...')
                    self.backup_media_files(backup_path)
                
                # 3. Backup configuration files
                self.stdout.write('⚙️ Backing up configuration...')
                self.backup_configuration(backup_path)
                
                # 4. Create backup manifest
                self.stdout.write('📋 Creating backup manifest...')
                self.create_backup_manifest(backup_path, timestamp)
                
                # 5. Compress if requested
                if options['compress']:
                    self.stdout.write('🗜️ Compressing backup...')
                    final_backup_path = self.compress_backup(backup_path, backup_dir, backup_name)
                else:
                    final_backup_path = backup_dir / backup_name
                    shutil.copytree(backup_path, final_backup_path)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Backup completed successfully!\n'
                        f'📦 Backup saved to: {final_backup_path}\n'
                        f'📊 Backup size: {self.get_size_format(self.get_dir_size(final_backup_path))}'
                    )
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Backup failed: {str(e)}')
                )
                raise

    def create_database_backup(self, backup_path):
        """Create a complete database backup"""
        db_backup_path = backup_path / 'database'
        db_backup_path.mkdir()
        
        # Create JSON fixture of all data
        fixture_file = db_backup_path / 'full_data.json'
        
        with open(fixture_file, 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                '--natural-foreign',
                '--natural-primary',
                '--indent=2',
                stdout=f,
                exclude=[
                    'contenttypes',
                    'auth.permission',
                    'sessions.session',
                    'admin.logentry',
                ]
            )
        
        # Create individual app backups for easier restoration
        apps_to_backup = [
            'users', 'courses', 'assignments', 'attendance', 
            'communications', 'fees', 'website', 'appointments'
        ]
        
        for app_name in apps_to_backup:
            try:
                app_file = db_backup_path / f'{app_name}_data.json'
                with open(app_file, 'w', encoding='utf-8') as f:
                    call_command(
                        'dumpdata',
                        app_name,
                        '--natural-foreign',
                        '--natural-primary',
                        '--indent=2',
                        stdout=f
                    )
                self.stdout.write(f'  ✓ Backed up {app_name} data')
            except Exception as e:
                self.stdout.write(f'  ⚠️ Warning: Could not backup {app_name}: {str(e)}')

    def backup_media_files(self, backup_path):
        """Backup all media files"""
        media_backup_path = backup_path / 'media'
        
        if hasattr(settings, 'MEDIA_ROOT') and os.path.exists(settings.MEDIA_ROOT):
            shutil.copytree(settings.MEDIA_ROOT, media_backup_path)
            file_count = sum([len(files) for r, d, files in os.walk(media_backup_path)])
            self.stdout.write(f'  ✓ Backed up {file_count} media files')
        else:
            self.stdout.write('  ⚠️ No media files found to backup')

    def backup_configuration(self, backup_path):
        """Backup configuration files and settings"""
        config_backup_path = backup_path / 'configuration'
        config_backup_path.mkdir()
        
        # Backup settings file (without sensitive data)
        settings_data = {
            'DEBUG': getattr(settings, 'DEBUG', False),
            'TIME_ZONE': getattr(settings, 'TIME_ZONE', 'UTC'),
            'LANGUAGE_CODE': getattr(settings, 'LANGUAGE_CODE', 'en-us'),
            'INSTALLED_APPS': getattr(settings, 'INSTALLED_APPS', []),
            'DATABASES_ENGINE': settings.DATABASES['default']['ENGINE'] if 'default' in settings.DATABASES else None,
            'STATIC_URL': getattr(settings, 'STATIC_URL', '/static/'),
            'MEDIA_URL': getattr(settings, 'MEDIA_URL', '/media/'),
        }
        
        with open(config_backup_path / 'django_settings.json', 'w') as f:
            json.dump(settings_data, f, indent=2)
        
        # Backup requirements if exists
        req_files = ['requirements.txt', 'requirements.pip', 'Pipfile']
        for req_file in req_files:
            req_path = Path(settings.BASE_DIR) / req_file
            if req_path.exists():
                shutil.copy2(req_path, config_backup_path)
                self.stdout.write(f'  ✓ Backed up {req_file}')

    def create_backup_manifest(self, backup_path, timestamp):
        """Create a manifest file with backup information"""
        manifest = {
            'backup_info': {
                'created_at': timestamp,
                'django_version': self.get_django_version(),
                'python_version': self.get_python_version(),
                'database_engine': settings.DATABASES['default']['ENGINE'],
                'backup_type': 'full_system_backup',
                'version': '1.0'
            },
            'contents': {
                'database': 'Complete database dump in JSON format',
                'media': 'All uploaded media files',
                'configuration': 'Django settings and requirements'
            },
            'restoration_notes': [
                '1. Restore database using: python manage.py loaddata database/full_data.json',
                '2. Copy media files to MEDIA_ROOT directory',
                '3. Review configuration files for any needed updates',
                '4. Run migrations if needed: python manage.py migrate',
                '5. Collect static files: python manage.py collectstatic'
            ]
        }
        
        with open(backup_path / 'BACKUP_MANIFEST.json', 'w') as f:
            json.dump(manifest, f, indent=2)

    def compress_backup(self, backup_path, output_dir, backup_name):
        """Compress the backup into a ZIP file"""
        zip_path = output_dir / f'{backup_name}.zip'
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(backup_path)
                    zipf.write(file_path, arc_path)
        
        return zip_path

    def get_django_version(self):
        """Get Django version"""
        import django
        return django.get_version()

    def get_python_version(self):
        """Get Python version"""
        import sys
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    def get_dir_size(self, path):
        """Get directory size in bytes"""
        if path.is_file():
            return path.stat().st_size
        
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                filepath = Path(dirpath) / filename
                total_size += filepath.stat().st_size
        return total_size

    def get_size_format(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
