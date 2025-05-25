from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    """Global site settings and content"""
    site_name = models.CharField(max_length=200, default="Deigratia Montessori School")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    site_description = models.TextField(blank=True)

    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # About Section
    about_section_title = models.CharField(max_length=200, default="Why Choose Us?")
    about_section_content = HTMLField(blank=True)

    # Gallery Settings
    show_gallery_carousel = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class PageSection(models.Model):
    """Reusable page sections"""
    SECTION_TYPES = [
        ('about_hero', 'About Hero Section'),
        ('mission', 'Mission Section'),
        ('vision', 'Vision Section'),
        ('story', 'Our Story Section'),
    ]

    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    content = HTMLField()
    image = models.ImageField(upload_to='page_content/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Page Section"
        verbose_name_plural = "Page Sections"

    def __str__(self):
        return f"{self.get_section_type_display()}"


class HeroSlide(models.Model):
    """Hero carousel slides"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='hero_slides/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return self.title


class Announcement(models.Model):
    """School announcements"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = HTMLField()
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:announcement-detail', kwargs={'slug': self.slug})


class EventCategory(models.Model):
    """Event categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """School events"""
    title = models.CharField(max_length=200)
    description = HTMLField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, blank=True, null=True)

    # Registration fields
    registration_required = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)

    # Integration with management system
    management_event = models.ForeignKey(
        'communications.Event',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Linked management system event'
    )

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"

    def get_absolute_url(self):
        return reverse('website:event-detail', kwargs={'pk': self.pk})

    @property
    def is_upcoming(self):
        return self.date > timezone.now()


class StaffMember(models.Model):
    """Staff members"""
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    bio = HTMLField()
    image = models.ImageField(upload_to='staff/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    # Additional fields for detailed profile
    qualification = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    interests = models.TextField(blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff Members"

    def __str__(self):
        return f"{self.name} - {self.position}"


class Testimonial(models.Model):
    """Parent/student testimonials"""
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, help_text="e.g., Parent of John Doe")
    content = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.role}"


class GalleryImage(models.Model):
    """Gallery images"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('website:gallery-detail', kwargs={'pk': self.pk})


class MontessoriItem(models.Model):
    """Montessori method features"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon name (without 'fa-')")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Montessori Item"
        verbose_name_plural = "Montessori Items"

    def __str__(self):
        return self.title


class Application(models.Model):
    """Student applications"""
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('waitlisted', 'Waitlisted'),
    ]

    # Student Information
    student_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    grade_applying_for = models.CharField(max_length=50)

    # Parent Information
    parent_name = models.CharField(max_length=200)
    parent_email = models.EmailField()
    parent_phone = models.CharField(max_length=20)
    address = models.TextField()

    # Application Details
    previous_school = models.CharField(max_length=200, blank=True)
    special_needs = models.TextField(blank=True)
    additional_info = models.TextField(blank=True)

    # Documents
    birth_certificate = models.FileField(upload_to='applications/', blank=True, null=True)
    previous_report = models.FileField(upload_to='applications/', blank=True, null=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Application"
        verbose_name_plural = "Applications"

    def __str__(self):
        return f"{self.student_name} - {self.get_status_display()}"
