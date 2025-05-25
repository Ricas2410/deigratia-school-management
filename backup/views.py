import os
import json
import zipfile
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.core.management import call_command
from django.conf import settings
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import BackupRecord, RestoreRecord, BackupSchedule
import threading
import tempfile
from io import StringIO

def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def backup_dashboard(request):
    """Main backup dashboard"""
    # Get recent backups
    recent_backups = BackupRecord.objects.all()[:10]
    
    # Get backup statistics
    total_backups = BackupRecord.objects.count()
    successful_backups = BackupRecord.objects.filter(status='completed').count()
    failed_backups = BackupRecord.objects.filter(status='failed').count()
    
    # Calculate total backup size
    total_size = sum([b.file_size for b in BackupRecord.objects.filter(file_size__isnull=False)])
    
    # Get scheduled backups
    scheduled_backups = BackupSchedule.objects.filter(is_active=True)
    
    context = {
        'recent_backups': recent_backups,
        'total_backups': total_backups,
        'successful_backups': successful_backups,
        'failed_backups': failed_backups,
        'total_size': total_size,
        'scheduled_backups': scheduled_backups,
    }
    
    return render(request, 'backup/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def backup_list(request):
    """List all backups with pagination"""
    backups = BackupRecord.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        backups = backups.filter(status=status_filter)
    
    # Filter by type if provided
    type_filter = request.GET.get('type')
    if type_filter:
        backups = backups.filter(backup_type=type_filter)
    
    # Pagination
    paginator = Paginator(backups, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'type_filter': type_filter,
    }
    
    return render(request, 'backup/backup_list.html', context)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def create_backup(request):
    """Create a new backup"""
    backup_type = request.POST.get('backup_type', 'full')
    include_media = request.POST.get('include_media') == 'on'
    include_database = request.POST.get('include_database') == 'on'
    compress_backup = request.POST.get('compress_backup', 'on') == 'on'
    notes = request.POST.get('notes', '')
    
    # Create backup record
    backup_record = BackupRecord.objects.create(
        name=f"Manual Backup {timezone.now().strftime('%Y-%m-%d %H:%M')}",
        backup_type=backup_type,
        status='pending',
        created_by=request.user,
        includes_database=include_database,
        includes_media=include_media,
        notes=notes
    )
    
    # Start backup in background thread
    def run_backup():
        try:
            backup_record.status = 'in_progress'
            backup_record.save()
            
            # Prepare command arguments
            cmd_args = ['--output-dir=backups']
            if include_media:
                cmd_args.append('--include-media')
            if compress_backup:
                cmd_args.append('--compress')
            
            # Capture command output
            output = StringIO()
            call_command('create_full_backup', *cmd_args, stdout=output)
            
            # Find the created backup file
            backup_dir = Path('backups')
            backup_files = list(backup_dir.glob(f'school_backup_*'))
            if backup_files:
                latest_backup = max(backup_files, key=os.path.getctime)
                file_size = latest_backup.stat().st_size if latest_backup.exists() else 0
                backup_record.mark_completed(str(latest_backup), file_size)
            else:
                backup_record.mark_failed("Backup file not found after creation")
                
        except Exception as e:
            backup_record.mark_failed(str(e))
    
    # Start backup thread
    backup_thread = threading.Thread(target=run_backup)
    backup_thread.daemon = True
    backup_thread.start()
    
    messages.success(request, f'Backup "{backup_record.name}" has been started. You can monitor its progress in the backup list.')
    return redirect('backup:backup_list')

@login_required
@user_passes_test(is_admin)
def backup_detail(request, backup_id):
    """Show backup details"""
    backup = get_object_or_404(BackupRecord, id=backup_id)
    
    # Get restore history for this backup
    restores = RestoreRecord.objects.filter(backup_record=backup)
    
    context = {
        'backup': backup,
        'restores': restores,
    }
    
    return render(request, 'backup/backup_detail.html', context)

@login_required
@user_passes_test(is_admin)
def download_backup(request, backup_id):
    """Download a backup file"""
    backup = get_object_or_404(BackupRecord, id=backup_id)
    
    if not backup.file_exists:
        raise Http404("Backup file not found")
    
    file_path = Path(backup.file_path)
    
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{file_path.name}"'
        return response

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def restore_backup(request, backup_id):
    """Restore from a backup"""
    backup = get_object_or_404(BackupRecord, id=backup_id)
    
    if not backup.file_exists:
        messages.error(request, "Backup file not found. Cannot restore.")
        return redirect('backup:backup_detail', backup_id=backup_id)
    
    restore_database = request.POST.get('restore_database') == 'on'
    restore_media = request.POST.get('restore_media') == 'on'
    notes = request.POST.get('notes', '')
    
    # Create restore record
    restore_record = RestoreRecord.objects.create(
        backup_record=backup,
        status='pending',
        initiated_by=request.user,
        restore_database=restore_database,
        restore_media=restore_media,
        notes=notes
    )
    
    # Start restore in background thread
    def run_restore():
        try:
            restore_record.status = 'in_progress'
            restore_record.save()
            
            # Prepare command arguments
            cmd_args = [backup.file_path]
            if restore_database:
                cmd_args.append('--restore-database')
            if restore_media:
                cmd_args.append('--restore-media')
            cmd_args.append('--force')  # Skip confirmation in background
            
            # Run restore command
            call_command('restore_full_backup', *cmd_args)
            
            restore_record.mark_completed()
            
        except Exception as e:
            restore_record.mark_failed(str(e))
    
    # Start restore thread
    restore_thread = threading.Thread(target=run_restore)
    restore_thread.daemon = True
    restore_thread.start()
    
    messages.success(request, f'Restore operation has been started. You can monitor its progress.')
    return redirect('backup:backup_detail', backup_id=backup_id)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def delete_backup(request, backup_id):
    """Delete a backup"""
    backup = get_object_or_404(BackupRecord, id=backup_id)
    
    # Delete the file if it exists
    if backup.file_exists:
        try:
            os.remove(backup.file_path)
        except OSError:
            pass  # File might already be deleted
    
    # Delete the record
    backup_name = backup.name
    backup.delete()
    
    messages.success(request, f'Backup "{backup_name}" has been deleted.')
    return redirect('backup:backup_list')

@login_required
@user_passes_test(is_admin)
def backup_status_api(request, backup_id):
    """API endpoint to check backup status"""
    backup = get_object_or_404(BackupRecord, id=backup_id)
    
    data = {
        'status': backup.status,
        'file_size': backup.file_size_formatted if backup.file_size else None,
        'completed_at': backup.completed_at.isoformat() if backup.completed_at else None,
        'error_message': backup.error_message,
    }
    
    return JsonResponse(data)

@login_required
@user_passes_test(is_admin)
def upload_backup(request):
    """Upload and register an external backup"""
    if request.method == 'POST':
        uploaded_file = request.FILES.get('backup_file')
        notes = request.POST.get('notes', '')
        
        if not uploaded_file:
            messages.error(request, 'Please select a backup file to upload.')
            return redirect('backup:backup_dashboard')
        
        # Save uploaded file
        backup_dir = Path('backups/uploaded')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = backup_dir / uploaded_file.name
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Create backup record
        backup_record = BackupRecord.objects.create(
            name=f"Uploaded: {uploaded_file.name}",
            backup_type='full',  # Assume full backup
            status='completed',
            created_by=request.user,
            file_path=str(file_path),
            file_size=uploaded_file.size,
            notes=notes,
            completed_at=timezone.now()
        )
        
        messages.success(request, f'Backup "{uploaded_file.name}" has been uploaded and registered.')
        return redirect('backup:backup_detail', backup_id=backup_record.id)
    
    return render(request, 'backup/upload_backup.html')
