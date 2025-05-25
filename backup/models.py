from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import os

User = get_user_model()

class BackupRecord(models.Model):
    """Model to track backup history and metadata"""
    
    BACKUP_TYPES = [
        ('full', 'Full System Backup'),
        ('database', 'Database Only'),
        ('media', 'Media Files Only'),
        ('settings', 'Settings Only'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    name = models.CharField(max_length=255, help_text="Backup name/identifier")
    backup_type = models.CharField(max_length=20, choices=BACKUP_TYPES, default='full')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # File information
    file_path = models.CharField(max_length=500, help_text="Path to backup file")
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Backup details
    includes_database = models.BooleanField(default=True)
    includes_media = models.BooleanField(default=True)
    includes_settings = models.BooleanField(default=True)
    
    # Statistics
    database_records = models.IntegerField(null=True, blank=True, help_text="Number of database records")
    media_files_count = models.IntegerField(null=True, blank=True, help_text="Number of media files")
    
    # Error information
    error_message = models.TextField(blank=True, help_text="Error message if backup failed")
    
    # Notes
    notes = models.TextField(blank=True, help_text="Additional notes about this backup")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Backup Record"
        verbose_name_plural = "Backup Records"
    
    def __str__(self):
        return f"{self.name} ({self.get_backup_type_display()}) - {self.status}"
    
    @property
    def file_exists(self):
        """Check if the backup file still exists"""
        return os.path.exists(self.file_path) if self.file_path else False
    
    @property
    def file_size_formatted(self):
        """Return formatted file size"""
        if not self.file_size:
            return "Unknown"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    @property
    def duration(self):
        """Return backup duration if completed"""
        if self.completed_at and self.created_at:
            return self.completed_at - self.created_at
        return None
    
    def mark_completed(self, file_path=None, file_size=None):
        """Mark backup as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        if file_path:
            self.file_path = file_path
        if file_size:
            self.file_size = file_size
        self.save()
    
    def mark_failed(self, error_message):
        """Mark backup as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.completed_at = timezone.now()
        self.save()


class RestoreRecord(models.Model):
    """Model to track restore operations"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    backup_record = models.ForeignKey(BackupRecord, on_delete=models.CASCADE, related_name='restores')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Restore options
    restore_database = models.BooleanField(default=True)
    restore_media = models.BooleanField(default=True)
    restore_settings = models.BooleanField(default=True)
    
    # Metadata
    initiated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    initiated_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Pre-restore backup
    pre_restore_backup = models.ForeignKey(
        BackupRecord, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='pre_restore_for'
    )
    
    # Error information
    error_message = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-initiated_at']
        verbose_name = "Restore Record"
        verbose_name_plural = "Restore Records"
    
    def __str__(self):
        return f"Restore of {self.backup_record.name} - {self.status}"
    
    @property
    def duration(self):
        """Return restore duration if completed"""
        if self.completed_at and self.initiated_at:
            return self.completed_at - self.initiated_at
        return None
    
    def mark_completed(self):
        """Mark restore as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_failed(self, error_message):
        """Mark restore as failed"""
        self.status = 'failed'
        self.error_message = error_message
        self.completed_at = timezone.now()
        self.save()


class BackupSchedule(models.Model):
    """Model for scheduled automatic backups"""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    name = models.CharField(max_length=255)
    backup_type = models.CharField(max_length=20, choices=BackupRecord.BACKUP_TYPES, default='full')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    
    # Schedule settings
    is_active = models.BooleanField(default=True)
    next_run = models.DateTimeField()
    last_run = models.DateTimeField(null=True, blank=True)
    
    # Backup options
    includes_database = models.BooleanField(default=True)
    includes_media = models.BooleanField(default=True)
    includes_settings = models.BooleanField(default=True)
    compress_backup = models.BooleanField(default=True)
    
    # Retention
    keep_backups = models.IntegerField(default=10, help_text="Number of backups to keep")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Backup Schedule"
        verbose_name_plural = "Backup Schedules"
    
    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"
