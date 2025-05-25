from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('academics/', views.academics, name='academics'),
    path('admissions/', views.admissions, name='admissions'),
    path('contact/', views.contact, name='contact'),
    
    # Events
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('calendar/', views.calendar, name='calendar'),
    
    # News & Announcements
    path('news/', views.news, name='news'),
    path('announcements/<slug:slug>/', views.announcement_detail, name='announcement-detail'),
    
    # Gallery
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:pk>/', views.gallery_detail, name='gallery-detail'),
    
    # Staff
    path('staff/', views.staff_list, name='staff-list'),
    
    # Other pages
    path('virtual-tour/', views.virtual_tour, name='virtual-tour'),
    path('career/', views.career, name='career'),
    path('faq/', views.faq, name='faq'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
    
    # API endpoints
    path('api/staff/<int:staff_id>/', views.staff_api, name='staff-api'),
]
