from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    HeroSlide, Announcement, Event, StaffMember,
    Testimonial, GalleryImage, MontessoriItem, Application
)
from .forms import ApplicationForm, ContactForm


def home(request):
    """Homepage view"""
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True)[:5],
        'announcements': Announcement.objects.filter(is_active=True, is_featured=True)[:3],
        'upcoming_events': Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()
        ).order_by('date')[:3],
        'testimonials': Testimonial.objects.filter(is_active=True, is_featured=True)[:3],
        'featured_gallery': GalleryImage.objects.filter(is_active=True, is_featured=True)[:6],
    }
    return render(request, 'website/home.html', context)


def about(request):
    """About page view"""
    context = {
        'staff_members': StaffMember.objects.filter(is_active=True, is_featured=True)[:6],
        'testimonials': Testimonial.objects.filter(is_active=True)[:3],
        'montessori_items': MontessoriItem.objects.filter(is_active=True)[:4],
    }
    return render(request, 'website/about.html', context)


def academics(request):
    """Academics page view"""
    return render(request, 'website/academics.html')


def admissions(request):
    """Admissions page view"""
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            messages.success(request, 'Your application has been submitted successfully!')

            # Send confirmation email
            try:
                send_mail(
                    'Application Received - Deigratia Montessori School',
                    f'Dear {application.parent_name},\n\nWe have received your application for {application.student_name}. We will review it and get back to you soon.\n\nThank you for your interest in our school.',
                    settings.DEFAULT_FROM_EMAIL,
                    [application.parent_email],
                    fail_silently=True,
                )
            except Exception:
                pass

            return redirect('website:admissions')
    else:
        form = ApplicationForm()

    return render(request, 'website/admissions.html', {'form': form})


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            try:
                send_mail(
                    f"Contact Form: {form.cleaned_data['subject']}",
                    f"From: {form.cleaned_data['name']} ({form.cleaned_data['email']})\n\n{form.cleaned_data['message']}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception:
                messages.error(request, 'There was an error sending your message. Please try again.')

            return redirect('website:contact')
    else:
        form = ContactForm()

    return render(request, 'website/contact.html', {'form': form})


def events(request):
    """Events listing page"""
    events_list = Event.objects.filter(is_active=True).order_by('date')
    paginator = Paginator(events_list, 12)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)

    return render(request, 'website/events.html', {'events': events_page})


def event_detail(request, pk):
    """Event detail page"""
    event = get_object_or_404(Event, pk=pk, is_active=True)
    return render(request, 'website/event_detail.html', {'event': event})


def announcement_detail(request, slug):
    """Announcement detail page"""
    announcement = get_object_or_404(Announcement, slug=slug, is_active=True)
    return render(request, 'website/announcement_detail.html', {'announcement': announcement})


def gallery(request):
    """Gallery page"""
    # Filter images
    images_list = GalleryImage.objects.filter(is_active=True)

    # Order by featured first, then by order, then by date
    images_list = images_list.order_by('-is_featured', 'order', '-created_at')

    # Pagination
    paginator = Paginator(images_list, 12)
    page_number = request.GET.get('page')
    images_page = paginator.get_page(page_number)

    context = {
        'galleries': images_page,  # Changed from 'images' to 'galleries' to match template
        'is_paginated': images_page.has_other_pages(),
        'page_obj': images_page,
    }

    return render(request, 'website/gallery.html', context)


def gallery_detail(request, pk):
    """Gallery image detail page"""
    gallery = get_object_or_404(GalleryImage, pk=pk, is_active=True)
    return render(request, 'website/gallery_detail.html', {'gallery': gallery})


def staff_list(request):
    """Staff listing page"""
    staff_members = StaffMember.objects.filter(is_active=True)
    return render(request, 'website/staff_list.html', {'staff_members': staff_members})


def news(request):
    """News/announcements page"""
    announcements_list = Announcement.objects.filter(is_active=True)
    paginator = Paginator(announcements_list, 10)
    page_number = request.GET.get('page')
    announcements_page = paginator.get_page(page_number)

    return render(request, 'website/news.html', {'announcements': announcements_page})


def calendar(request):
    """Calendar page"""
    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')

    return render(request, 'website/calendar.html', {'upcoming_events': upcoming_events})


def virtual_tour(request):
    """Virtual tour page"""
    return render(request, 'website/virtual_tour.html')


def career(request):
    """Career page"""
    return render(request, 'website/career.html')


def faq(request):
    """FAQ page"""
    return render(request, 'website/faq.html')


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'website/privacy_policy.html')


def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'website/terms_of_service.html')


# API Views
@require_http_methods(["GET"])
def staff_api(request, staff_id):
    """API endpoint for staff details"""
    try:
        staff = get_object_or_404(StaffMember, id=staff_id, is_active=True)
        data = {
            'id': staff.id,
            'name': staff.name,
            'position': staff.position,
            'bio': staff.bio,
            'email': staff.email,
            'phone': staff.phone,
            'qualification': staff.qualification,
            'achievements': staff.achievements,
            'interests': staff.interests,
            'image_url': staff.image.url if staff.image else '',
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': 'Staff member not found'}, status=404)
