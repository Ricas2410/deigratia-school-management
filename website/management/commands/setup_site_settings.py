from django.core.management.base import BaseCommand
from website.models import SiteSettings


class Command(BaseCommand):
    help = 'Create default site settings'

    def handle(self, *args, **options):
        # Check if settings already exist
        if SiteSettings.objects.exists():
            self.stdout.write(
                self.style.WARNING('Site settings already exist. Use admin panel to modify them.')
            )
            return

        # Create default settings
        settings = SiteSettings.objects.create(
            site_name="Deigratia Montessori School",
            site_description="Excellence in education through the Montessori method, nurturing each child's unique potential.",
            phone="+1 (555) 123-4567",
            email="info@deigratiamontessori.edu",
            address="123 Education Street, Learning City, LC 12345",
            facebook_url="https://facebook.com/deigratiamontessori",
            twitter_url="https://twitter.com/deigratiamontessori",
            instagram_url="https://instagram.com/deigratiamontessori",
            about_section_title="Why Choose Deigratia Montessori School?",
            about_section_content="""
            <p>At Deigratia Montessori School, we believe in nurturing the whole child through the proven Montessori method. Our approach focuses on:</p>
            <ul>
                <li>Child-centered learning environment</li>
                <li>Mixed-age classrooms that foster peer learning</li>
                <li>Hands-on learning materials</li>
                <li>Respect for the child's natural development</li>
                <li>Experienced and certified Montessori educators</li>
            </ul>
            """,
            show_gallery_carousel=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created site settings: {settings.site_name}')
        )
