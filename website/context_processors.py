from django.conf import settings as django_settings
from .models import SiteSettings, PageSection


def site_settings(request):
    """
    Context processor to make site settings available in all templates
    """
    try:
        settings = SiteSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = SiteSettings.objects.create()
    except Exception:
        # Fallback in case of database issues
        settings = None

    # Get school settings for logo and other shared data
    school_settings = None
    try:
        from users.models import SchoolSettings
        school_settings = SchoolSettings.objects.first()
    except Exception:
        pass

    # Get page sections
    sections = {}
    try:
        for section in PageSection.objects.filter(is_active=True):
            sections[section.section_type] = section
    except Exception:
        pass

    # Determine which logo to use (prioritize school settings logo)
    logo_url = None
    if school_settings and school_settings.logo:
        logo_url = school_settings.logo.url
    elif settings and settings.site_logo:
        logo_url = settings.site_logo.url

    # Determine site name (prioritize school settings)
    site_name = django_settings.DEFAULT_SCHOOL_NAME
    if school_settings and school_settings.school_name:
        site_name = school_settings.school_name
    elif settings and settings.site_name:
        site_name = settings.site_name

    return {
        'settings': settings,
        'school_settings': school_settings,
        'sections': sections,
        'site_name': site_name,
        'logo_url': logo_url,
    }
