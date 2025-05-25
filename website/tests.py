from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import (
    SiteSettings, HeroSlide, Announcement, Event,
    StaffMember, Testimonial, GalleryImage, Application
)


class WebsiteModelsTest(TestCase):
    """Test website models"""
    
    def setUp(self):
        self.site_settings = SiteSettings.objects.create(
            site_name="Test School",
            email="test@school.com"
        )
    
    def test_site_settings_creation(self):
        """Test SiteSettings model creation"""
        self.assertEqual(self.site_settings.site_name, "Test School")
        self.assertEqual(str(self.site_settings), "Test School")
    
    def test_hero_slide_creation(self):
        """Test HeroSlide model creation"""
        slide = HeroSlide.objects.create(
            title="Test Slide",
            subtitle="Test Subtitle"
        )
        self.assertEqual(str(slide), "Test Slide")
    
    def test_announcement_slug_generation(self):
        """Test automatic slug generation for announcements"""
        announcement = Announcement.objects.create(
            title="Test Announcement",
            content="Test content"
        )
        self.assertEqual(announcement.slug, "test-announcement")


class WebsiteViewsTest(TestCase):
    """Test website views"""
    
    def setUp(self):
        self.client = Client()
        self.site_settings = SiteSettings.objects.create(
            site_name="Test School"
        )
    
    def test_home_page(self):
        """Test home page loads correctly"""
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test School")
    
    def test_about_page(self):
        """Test about page loads correctly"""
        response = self.client.get(reverse('website:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_contact_page(self):
        """Test contact page loads correctly"""
        response = self.client.get(reverse('website:contact'))
        self.assertEqual(response.status_code, 200)
    
    def test_admissions_page(self):
        """Test admissions page loads correctly"""
        response = self.client.get(reverse('website:admissions'))
        self.assertEqual(response.status_code, 200)


class ApplicationFormTest(TestCase):
    """Test application form submission"""
    
    def setUp(self):
        self.client = Client()
    
    def test_application_submission(self):
        """Test valid application submission"""
        form_data = {
            'student_name': 'John Doe',
            'date_of_birth': '2015-01-01',
            'grade_applying_for': 'kindergarten',
            'parent_name': 'Jane Doe',
            'parent_email': 'jane@example.com',
            'parent_phone': '+1234567890',
            'address': '123 Main St, City, State',
        }
        
        response = self.client.post(reverse('website:admissions'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission
        
        # Check if application was created
        self.assertTrue(Application.objects.filter(student_name='John Doe').exists())
