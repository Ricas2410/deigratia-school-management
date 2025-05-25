import os
import json
import zipfile
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.db import transaction
import tempfile

class Command(BaseCommand):
    help = 'Restore a comprehensive backup of school data including database, media files, and settings'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_path',
            type=str,
            help='Path to backup file (.zip) or backup directory'
        )
        parser.add_argument(
            '--restore-media',
            action='store_true',
            default=True,
            help='Restore media files (default: True)'
        )
        parser.add_argument(
            '--restore-database',
            action='store_true',
            default=True,
            help='Restore database (default: True)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force restoration without confirmation prompts'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be restored without actually doing it'
        )

    def handle(self, *args, **options):
        backup_path = Path(options['backup_path'])
        
        if not backup_path.exists():
            self.stdout.write(self.style.ERROR(f'❌ Backup path does not exist: {backup_path}'))
            return
        
        self.stdout.write(self.style.SUCCESS('🔄 Starting school data restoration...'))
        
        # Handle ZIP files
        if backup_path.suffix == '.zip':
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                self.stdout.write('📦 Extracting backup archive...')
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(temp_path)
                
                # Find the backup directory inside
                backup_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
                if not backup_dirs:
                    self.stdout.write(self.style.ERROR('❌ No backup directory found in archive'))
                    return
                
                extracted_backup_path = backup_dirs[0]
                self.perform_restoration(extracted_backup_path, options)
        else:
            self.perform_restoration(backup_path, options)

    def perform_restoration(self, backup_path, options):
        """Perform the actual restoration process"""
        
        # Validate backup
        if not self.validate_backup(backup_path):
            return
        
        # Load manifest
        manifest = self.load_manifest(backup_path)
        if manifest:
            self.stdout.write(f'📋 Backup created: {manifest["backup_info"]["created_at"]}')
            self.stdout.write(f'🐍 Python version: {manifest["backup_info"]["python_version"]}')
            self.stdout.write(f'🎯 Django version: {manifest["backup_info"]["django_version"]}')
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No changes will be made'))
            self.show_restoration_plan(backup_path, options)
            return
        
        # Confirmation prompt
        if not options['force']:
            if not self.confirm_restoration():
                self.stdout.write('❌ Restoration cancelled by user')
                return
        
        try:
            # Create backup of current state before restoration
            self.stdout.write('💾 Creating backup of current state...')
            self.create_pre_restoration_backup()
            
            # Restore database
            if options['restore_database']:
                self.stdout.write('📊 Restoring database...')
                self.restore_database(backup_path)
            
            # Restore media files
            if options['restore_media']:
                self.stdout.write('📁 Restoring media files...')
                self.restore_media_files(backup_path)
            
            # Run post-restoration tasks
            self.stdout.write('🔧 Running post-restoration tasks...')
            self.run_post_restoration_tasks()
            
            self.stdout.write(
                self.style.SUCCESS(
                    '✅ Restoration completed successfully!\n'
                    '🔄 Please restart your Django server to ensure all changes take effect.'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Restoration failed: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING(
                    '⚠️ A backup of your current state was created before restoration.\n'
                    'Check the backups directory if you need to recover.'
                )
            )
            raise

    def validate_backup(self, backup_path):
        """Validate that the backup is complete and valid"""
        required_files = ['BACKUP_MANIFEST.json']
        required_dirs = ['database']
        
        for file in required_files:
            if not (backup_path / file).exists():
                self.stdout.write(self.style.ERROR(f'❌ Missing required file: {file}'))
                return False
        
        for dir_name in required_dirs:
            if not (backup_path / dir_name).exists():
                self.stdout.write(self.style.ERROR(f'❌ Missing required directory: {dir_name}'))
                return False
        
        self.stdout.write('✅ Backup validation passed')
        return True

    def load_manifest(self, backup_path):
        """Load and return the backup manifest"""
        manifest_path = backup_path / 'BACKUP_MANIFEST.json'
        try:
            with open(manifest_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️ Could not load manifest: {str(e)}'))
            return None

    def show_restoration_plan(self, backup_path, options):
        """Show what would be restored in dry-run mode"""
        self.stdout.write('\n📋 RESTORATION PLAN:')
        
        if options['restore_database']:
            db_path = backup_path / 'database'
            if db_path.exists():
                json_files = list(db_path.glob('*.json'))
                self.stdout.write(f'  📊 Database: {len(json_files)} data files would be restored')
        
        if options['restore_media']:
            media_path = backup_path / 'media'
            if media_path.exists():
                file_count = sum([len(files) for r, d, files in os.walk(media_path)])
                self.stdout.write(f'  📁 Media: {file_count} files would be restored')
        
        config_path = backup_path / 'configuration'
        if config_path.exists():
            config_files = list(config_path.glob('*'))
            self.stdout.write(f'  ⚙️ Configuration: {len(config_files)} files available')

    def confirm_restoration(self):
        """Ask user for confirmation before proceeding"""
        self.stdout.write(
            self.style.WARNING(
                '\n⚠️  WARNING: This will overwrite your current data!\n'
                'A backup of your current state will be created first.\n'
            )
        )
        
        response = input('Do you want to proceed? (yes/no): ').lower().strip()
        return response in ['yes', 'y']

    def create_pre_restoration_backup(self):
        """Create a backup of current state before restoration"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'pre_restoration_backup_{timestamp}'
        
        # Use the backup command to create current state backup
        call_command('create_full_backup', '--output-dir=backups/pre_restoration')

    def restore_database(self, backup_path):
        """Restore database from backup"""
        db_path = backup_path / 'database'
        
        # First, try to restore from full_data.json
        full_data_file = db_path / 'full_data.json'
        if full_data_file.exists():
            self.stdout.write('  📊 Restoring from full database backup...')
            with transaction.atomic():
                # Clear existing data (be careful!)
                self.stdout.write('  🗑️ Clearing existing data...')
                call_command('flush', '--noinput')
                
                # Load the backup data
                call_command('loaddata', str(full_data_file))
                self.stdout.write('  ✅ Database restored successfully')
        else:
            # Restore from individual app files
            self.stdout.write('  📊 Restoring from individual app backups...')
            json_files = sorted(db_path.glob('*_data.json'))
            
            if not json_files:
                self.stdout.write(self.style.ERROR('  ❌ No database backup files found'))
                return
            
            with transaction.atomic():
                # Clear existing data
                self.stdout.write('  🗑️ Clearing existing data...')
                call_command('flush', '--noinput')
                
                # Load each app's data
                for json_file in json_files:
                    try:
                        call_command('loaddata', str(json_file))
                        self.stdout.write(f'  ✅ Restored {json_file.name}')
                    except Exception as e:
                        self.stdout.write(f'  ⚠️ Warning: Could not restore {json_file.name}: {str(e)}')

    def restore_media_files(self, backup_path):
        """Restore media files from backup"""
        media_backup_path = backup_path / 'media'
        
        if not media_backup_path.exists():
            self.stdout.write('  ⚠️ No media files to restore')
            return
        
        media_root = Path(settings.MEDIA_ROOT)
        
        # Backup existing media if it exists
        if media_root.exists():
            backup_media_path = media_root.parent / f'media_backup_{int(datetime.now().timestamp())}'
            shutil.move(str(media_root), str(backup_media_path))
            self.stdout.write(f'  💾 Existing media backed up to: {backup_media_path}')
        
        # Restore media files
        shutil.copytree(media_backup_path, media_root)
        file_count = sum([len(files) for r, d, files in os.walk(media_root)])
        self.stdout.write(f'  ✅ Restored {file_count} media files')

    def run_post_restoration_tasks(self):
        """Run necessary tasks after restoration"""
        try:
            # Run migrations to ensure database is up to date
            self.stdout.write('  🔄 Running database migrations...')
            call_command('migrate', '--run-syncdb')
            
            # Collect static files
            self.stdout.write('  📦 Collecting static files...')
            call_command('collectstatic', '--noinput', '--clear')
            
            self.stdout.write('  ✅ Post-restoration tasks completed')
            
        except Exception as e:
            self.stdout.write(f'  ⚠️ Warning: Some post-restoration tasks failed: {str(e)}')
            self.stdout.write('  💡 You may need to run these manually:')
            self.stdout.write('     - python manage.py migrate')
            self.stdout.write('     - python manage.py collectstatic')
