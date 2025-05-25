from django.urls import path
from . import views

app_name = 'backup'

urlpatterns = [
    # Dashboard
    path('', views.backup_dashboard, name='backup_dashboard'),
    
    # Backup management
    path('list/', views.backup_list, name='backup_list'),
    path('create/', views.create_backup, name='create_backup'),
    path('upload/', views.upload_backup, name='upload_backup'),
    
    # Backup details and actions
    path('<int:backup_id>/', views.backup_detail, name='backup_detail'),
    path('<int:backup_id>/download/', views.download_backup, name='download_backup'),
    path('<int:backup_id>/restore/', views.restore_backup, name='restore_backup'),
    path('<int:backup_id>/delete/', views.delete_backup, name='delete_backup'),
    
    # API endpoints
    path('api/<int:backup_id>/status/', views.backup_status_api, name='backup_status_api'),
]
