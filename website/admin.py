from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, PageSection, HeroSlide, Announcement, Event, EventCategory,
    StaffMember, Testimonial, GalleryImage, MontessoriItem, Application
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'email', 'phone', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_logo', 'site_description')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('About Section', {
            'fields': ('about_section_title', 'about_section_content')
        }),
        ('Gallery Settings', {
            'fields': ('show_gallery_carousel',)
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()


@admin.register(PageSection)
class PageSectionAdmin(admin.ModelAdmin):
    list_display = ['section_type', 'title', 'is_active', 'updated_at']
    list_filter = ['section_type', 'is_active']
    search_fields = ['title', 'content']

    def has_add_permission(self, request):
        # Check if all section types are already created
        existing_types = set(PageSection.objects.values_list('section_type', flat=True))
        available_types = set(dict(PageSection.SECTION_TYPES).keys())
        return len(existing_types) < len(available_types)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    ordering = ['order', 'created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'category', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active', 'date', 'registration_required']
    search_fields = ['title', 'description', 'location']
    ordering = ['date']
    date_hierarchy = 'date'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'date', 'location', 'image', 'category')
        }),
        ('Registration', {
            'fields': ('registration_required', 'registration_link', 'registration_deadline')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('System Integration', {
            'fields': ('management_event',),
            'classes': ('collapse',)
        }),
    )


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'is_featured', 'is_active', 'order']
    list_filter = ['is_featured', 'is_active', 'position']
    search_fields = ['name', 'position', 'bio']
    ordering = ['order', 'name']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'image')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Additional Details', {
            'fields': ('qualification', 'achievements', 'interests')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_featured', 'is_active', 'order']
    list_filter = ['is_featured', 'is_active']
    search_fields = ['name', 'role', 'content']
    ordering = ['order', 'created_at']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'is_active', 'image_preview', 'order']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['order', 'created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(MontessoriItem)
class MontessoriItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order', 'created_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'parent_name', 'grade_applying_for', 'status', 'created_at']
    list_filter = ['status', 'grade_applying_for', 'created_at']
    search_fields = ['student_name', 'parent_name', 'parent_email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'date_of_birth', 'grade_applying_for')
        }),
        ('Parent Information', {
            'fields': ('parent_name', 'parent_email', 'parent_phone', 'address')
        }),
        ('Application Details', {
            'fields': ('previous_school', 'special_needs', 'additional_info')
        }),
        ('Documents', {
            'fields': ('birth_certificate', 'previous_report')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_accepted', 'mark_as_rejected', 'mark_as_under_review']

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='accepted')
        self.message_user(request, f"{queryset.count()} applications marked as accepted.")
    mark_as_accepted.short_description = "Mark selected applications as accepted"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications marked as rejected.")
    mark_as_rejected.short_description = "Mark selected applications as rejected"

    def mark_as_under_review(self, request, queryset):
        queryset.update(status='under_review')
        self.message_user(request, f"{queryset.count()} applications marked as under review.")
    mark_as_under_review.short_description = "Mark selected applications as under review"
