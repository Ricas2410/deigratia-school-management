from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import os
import json

class Command(BaseCommand):
    help = 'Migrate data from local development to production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='JSON fixture file to load',
            required=True
        )
        parser.add_argument(
            '--backup',
            action='store_true',
            help='Create backup before loading data',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before loading (DANGEROUS)',
        )

    def handle(self, *args, **options):
        fixture_file = options['file']
        
        if not os.path.exists(fixture_file):
            self.stdout.write(
                self.style.ERROR(f'Fixture file {fixture_file} does not exist')
            )
            return

        # Create backup if requested
        if options['backup']:
            self.stdout.write('Creating database backup...')
            try:
                call_command('dumpdata', 
                           '--natural-foreign', 
                           '--natural-primary',
                           '--output=backup_before_migration.json')
                self.stdout.write(
                    self.style.SUCCESS('Backup created: backup_before_migration.json')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Backup failed: {str(e)}')
                )
                return

        # Clear data if requested
        if options['clear']:
            self.stdout.write(
                self.style.WARNING('This will DELETE all existing data!')
            )
            confirm = input('Type "yes" to continue: ')
            if confirm.lower() != 'yes':
                self.stdout.write('Migration cancelled.')
                return
            
            self.stdout.write('Clearing existing data...')
            # Add apps to clear in reverse dependency order
            apps_to_clear = [
                'assignments',
                'attendance', 
                'communications',
                'courses',
                'fees',
                'payroll',
                'appointments',
                'users',
                'website'
            ]
            
            for app in apps_to_clear:
                try:
                    call_command('flush', '--noinput', verbosity=0)
                    break
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Could not clear {app}: {str(e)}')
                    )

        # Load the fixture data
        self.stdout.write(f'Loading data from {fixture_file}...')
        
        try:
            with transaction.atomic():
                call_command('loaddata', fixture_file, verbosity=2)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded data from {fixture_file}')
            )
            
            # Run migrations to ensure everything is up to date
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS('Data migration completed successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Migration failed: {str(e)}')
            )
            
            if options['backup']:
                self.stdout.write(
                    'You can restore from backup using:'
                )
                self.stdout.write(
                    'python manage.py loaddata backup_before_migration.json'
                )
