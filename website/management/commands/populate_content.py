from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify

from website.models import (
    HeroSlide, GalleryImage, StaffMember, Event, EventCategory,
    Announcement, Testimonial, PageSection, SiteSettings
)

class Command(BaseCommand):
    help = 'Populate website content using existing images in media folder'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting website content population...")
        self.stdout.write("=" * 50)

        try:
            self.populate_hero_slides()
            self.populate_gallery()
            self.populate_staff()
            self.populate_events()
            self.populate_announcements()
            self.populate_testimonials()
            self.populate_page_sections()

            self.stdout.write("\n" + "=" * 50)
            self.stdout.write(self.style.SUCCESS("✅ Website content population completed successfully!"))
            self.stdout.write(f"\nYour website now has:")
            self.stdout.write(f"- {HeroSlide.objects.count()} Hero slides")
            self.stdout.write(f"- {GalleryImage.objects.count()} Gallery images")
            self.stdout.write(f"- {StaffMember.objects.count()} Staff members")
            self.stdout.write(f"- {Event.objects.count()} Events")
            self.stdout.write(f"- {Announcement.objects.count()} Announcements")
            self.stdout.write(f"- {Testimonial.objects.count()} Testimonials")
            self.stdout.write(f"- {PageSection.objects.count()} Page sections")

            self.stdout.write("\n🌟 Your images are now being used across the website!")
            self.stdout.write("Visit your website to see all the content in action.")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n❌ Error occurred: {str(e)}"))
            import traceback
            traceback.print_exc()

    def populate_hero_slides(self):
        """Populate hero slides with existing images"""
        self.stdout.write("Creating hero slides...")

        hero_data = [
            {
                'title': 'Welcome to Deigratia Montessori School',
                'subtitle': 'Nurturing Excellence Through Montessori Education',
                'image': 'hero_slides/Cultural_Dance_at_Montessori_school_in_Ghana.png',
                'order': 1
            },
            {
                'title': 'Modern Learning Environment',
                'subtitle': 'State-of-the-art computer lab for digital literacy',
                'image': 'hero_slides/Montessori_school_computer_lab_in_Ghana_1.png',
                'order': 2
            },
            {
                'title': 'STEM Education Excellence',
                'subtitle': 'Hands-on robotics and technology learning',
                'image': 'hero_slides/Montessori_school_robotics_class_in_Ghana.png',
                'order': 3
            },
            {
                'title': 'Inspiring Young Minds',
                'subtitle': 'Creating tomorrow\'s leaders through quality education',
                'image': 'hero_slides/youn-girl_in-class.png',
                'order': 4
            },
            {
                'title': 'Bright Futures Start Here',
                'subtitle': 'Where every child\'s potential is nurtured and celebrated',
                'image': 'hero_slides/sunshine_hero.png',
                'order': 5
            }
        ]

        for data in hero_data:
            slide, created = HeroSlide.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created hero slide: {slide.title}")
            else:
                self.stdout.write(f"- Hero slide already exists: {slide.title}")

    def populate_gallery(self):
        """Populate gallery with existing images"""
        self.stdout.write("\nCreating gallery images...")

        gallery_data = [
            {
                'title': 'Robotics Class in Action',
                'description': 'Students learning robotics and programming in our modern STEM lab',
                'image': 'gallery/Montessori_school_robotics_class_in_Ghana.png',
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Creative Learning Spaces',
                'description': 'Our beautifully designed classrooms inspire creativity and learning',
                'image': 'gallery/deepimg-1743926001836.png',
                'is_featured': True,
                'order': 2
            },
            {
                'title': 'Interactive Learning',
                'description': 'Students engaged in hands-on learning activities',
                'image': 'gallery/image_2.png',
                'is_featured': True,
                'order': 3
            },
            {
                'title': 'Outdoor Play Time',
                'description': 'Children enjoying outdoor activities and games',
                'image': 'gallery/kids_playing.jpg',
                'is_featured': False,
                'order': 4
            },
            {
                'title': 'Study Environment',
                'description': 'Comfortable and conducive study spaces for focused learning',
                'image': 'gallery/study-table.jpg',
                'is_featured': False,
                'order': 5
            },
            {
                'title': 'Art and Creativity',
                'description': 'Students expressing themselves through art and creative projects',
                'image': 'gallery/openart-image__Wev2ik8_1743926033245_raw.jpg',
                'is_featured': False,
                'order': 6
            },
            {
                'title': 'Learning Together',
                'description': 'Collaborative learning in our Montessori environment',
                'image': 'gallery/openart-image_yJvciICT_1743926033149_raw.jpg',
                'is_featured': False,
                'order': 7
            }
        ]

        for data in gallery_data:
            image, created = GalleryImage.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created gallery image: {image.title}")
            else:
                self.stdout.write(f"- Gallery image already exists: {image.title}")

    def populate_staff(self):
        """Populate staff members with existing images"""
        self.stdout.write("\nCreating staff members...")

        staff_data = [
            {
                'name': 'Dr. Kwame Nkrumah',
                'position': 'School Director',
                'bio': 'Dr. Nkrumah brings over 20 years of experience in Montessori education. He holds a PhD in Educational Leadership and is passionate about creating nurturing learning environments for children.',
                'image': 'staff/Kwame-Nkrumah-1024x1024.jpg',
                'email': 'director@deigratiamontessori.edu',
                'phone': '+233 24 123 4567',
                'qualification': 'PhD in Educational Leadership, AMI Montessori Diploma',
                'achievements': 'Published researcher in child development, Former UNESCO education consultant',
                'interests': 'Child psychology, Educational innovation, Community development',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Mrs. Sarah Asante',
                'position': 'Head of Primary School',
                'bio': 'Mrs. Asante is a certified Montessori educator with 15 years of experience. She specializes in early childhood development and curriculum design.',
                'image': 'staff/director.jpg',
                'email': 'primary@deigratiamontessori.edu',
                'phone': '+233 24 234 5678',
                'qualification': 'Masters in Early Childhood Education, AMI Primary Diploma',
                'achievements': 'Award-winning educator, Curriculum development specialist',
                'interests': 'Child development, Reading programs, Teacher training',
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Mr. John Mensah',
                'position': 'STEM Coordinator',
                'bio': 'Mr. Mensah leads our innovative STEM programs, bringing technology and hands-on learning to our students through robotics and computer science.',
                'image': 'staff/Image1.png',
                'email': 'stem@deigratiamontessori.edu',
                'phone': '+233 24 345 6789',
                'qualification': 'BSc Computer Science, Robotics Education Certificate',
                'achievements': 'Robotics competition coach, Technology integration specialist',
                'interests': 'Robotics, Programming, Educational technology',
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Ms. Grace Osei',
                'position': 'Art & Creative Director',
                'bio': 'Ms. Osei nurtures creativity and artistic expression in our students through various art programs and creative learning activities.',
                'image': 'staff/image3.jpg',
                'email': 'arts@deigratiamontessori.edu',
                'phone': '+233 24 456 7890',
                'qualification': 'BFA Fine Arts, Montessori Arts Integration Certificate',
                'achievements': 'Student art exhibition organizer, Creative curriculum developer',
                'interests': 'Visual arts, Creative expression, Art therapy',
                'is_featured': False,
                'order': 4
            }
        ]

        for data in staff_data:
            staff, created = StaffMember.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created staff member: {staff.name}")
            else:
                self.stdout.write(f"- Staff member already exists: {staff.name}")

    def populate_events(self):
        """Populate events with existing images"""
        self.stdout.write("\nCreating event categories and events...")

        # Create event categories first
        categories_data = [
            {'name': 'Academic Events', 'description': 'Educational and academic activities', 'color': '#007bff'},
            {'name': 'Science & Technology', 'description': 'STEM related events and activities', 'color': '#28a745'},
            {'name': 'Cultural Events', 'description': 'Cultural celebrations and activities', 'color': '#ffc107'},
            {'name': 'Sports & Recreation', 'description': 'Sports and recreational activities', 'color': '#dc3545'},
        ]

        for cat_data in categories_data:
            category, created = EventCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f"✓ Created event category: {category.name}")

        # Create events
        science_category = EventCategory.objects.get(name='Science & Technology')
        academic_category = EventCategory.objects.get(name='Academic Events')

        events_data = [
            {
                'title': 'Annual Science Day',
                'description': 'Join us for our exciting Annual Science Day where students showcase their scientific projects and experiments. A day filled with discovery, innovation, and hands-on learning experiences.',
                'date': timezone.now() + timedelta(days=30),
                'location': 'School Science Laboratory',
                'image': 'events/science_day.jpg',
                'category': science_category,
                'registration_required': True,
                'registration_link': 'https://forms.google.com/science-day',
                'registration_deadline': timezone.now() + timedelta(days=25),
                'is_featured': True
            },
            {
                'title': 'Innovation & Technology Fair',
                'description': 'Students present their innovative technology projects and robotics creations. Come see the future innovators in action!',
                'date': timezone.now() + timedelta(days=45),
                'location': 'School Auditorium',
                'image': 'events/inovate.webp',
                'category': science_category,
                'registration_required': False,
                'is_featured': True
            },
            {
                'title': 'School Exhibition',
                'description': 'Annual school exhibition showcasing student work, achievements, and school programs. Parents and community members are welcome.',
                'date': timezone.now() + timedelta(days=60),
                'location': 'School Grounds',
                'image': 'events/deepimg-1744835543039.png',
                'category': academic_category,
                'registration_required': False,
                'is_featured': False
            }
        ]

        for data in events_data:
            event, created = Event.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created event: {event.title}")
            else:
                self.stdout.write(f"- Event already exists: {event.title}")

    def populate_announcements(self):
        """Populate announcements with existing images"""
        self.stdout.write("\nCreating announcements...")

        announcements_data = [
            {
                'title': 'School Exhibition 2025 - Showcase of Excellence',
                'content': '''
                <p>We are excited to announce our annual School Exhibition taking place next month! This is a wonderful opportunity for our students to showcase their learning journey and achievements throughout the academic year.</p>

                <h4>Event Highlights:</h4>
                <ul>
                    <li>Student project displays from all grade levels</li>
                    <li>Science experiments and demonstrations</li>
                    <li>Art and creative works exhibition</li>
                    <li>Technology and robotics showcase</li>
                    <li>Cultural performances</li>
                </ul>

                <p>Parents, families, and community members are cordially invited to attend this celebration of learning and achievement.</p>
                ''',
                'image': 'announcements/School_exhibition.png',
                'is_featured': True,
                'slug': 'school-exhibition-2025'
            },
            {
                'title': 'Science Day Celebration - Exploring the Wonders of Science',
                'content': '''
                <p>Join us for an exciting Science Day celebration where our young scientists will demonstrate their understanding of scientific concepts through hands-on experiments and presentations.</p>

                <h4>Activities Include:</h4>
                <ul>
                    <li>Interactive science experiments</li>
                    <li>Student-led demonstrations</li>
                    <li>Science fair projects</li>
                    <li>Guest scientist presentations</li>
                    <li>Fun science games and activities</li>
                </ul>

                <p>This event promotes scientific thinking and curiosity among our students while making learning fun and engaging.</p>
                ''',
                'image': 'announcements/sciencedayImage.png',
                'is_featured': True,
                'slug': 'science-day-celebration'
            },
            {
                'title': 'New STEM Laboratory Now Open',
                'content': '''
                <p>We are thrilled to announce the opening of our new state-of-the-art STEM laboratory! This modern facility will enhance our students' learning experience in Science, Technology, Engineering, and Mathematics.</p>

                <h4>Laboratory Features:</h4>
                <ul>
                    <li>Advanced robotics equipment</li>
                    <li>Computer programming stations</li>
                    <li>3D printing capabilities</li>
                    <li>Interactive science equipment</li>
                    <li>Collaborative learning spaces</li>
                </ul>

                <p>This investment in our infrastructure demonstrates our commitment to providing world-class education for our students.</p>
                ''',
                'image': 'announcements/c4d71a65-4906-41c5-8f77-842084475778.png',
                'is_featured': False,
                'slug': 'new-stem-laboratory-open'
            }
        ]

        for data in announcements_data:
            announcement, created = Announcement.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created announcement: {announcement.title}")
            else:
                self.stdout.write(f"- Announcement already exists: {announcement.title}")

    def populate_testimonials(self):
        """Populate testimonials"""
        self.stdout.write("\nCreating testimonials...")

        testimonials_data = [
            {
                'name': 'Mrs. Akosua Mensah',
                'role': 'Parent of Kofi (Grade 3)',
                'content': 'Deigratia Montessori School has been a blessing for our family. The teachers are incredibly dedicated, and the Montessori approach has helped my son develop independence and a love for learning. I highly recommend this school to any parent looking for quality education.',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Mr. Samuel Asante',
                'role': 'Parent of Ama (Grade 2)',
                'content': 'The individual attention each child receives at Deigratia is remarkable. My daughter has grown so much in confidence and academic ability. The school truly understands child development and creates an environment where children thrive.',
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Mrs. Grace Osei',
                'role': 'Parent of Kwame (Grade 4)',
                'content': 'What sets Deigratia apart is their commitment to the whole child. Not only has my son excelled academically, but he has also developed strong social skills and emotional intelligence. The STEM programs are particularly impressive.',
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Dr. Emmanuel Boateng',
                'role': 'Parent of Adwoa (Grade 1)',
                'content': 'As an educator myself, I appreciate the professional approach and genuine care the teachers show. The Montessori method is implemented beautifully here, and I can see the positive impact on my daughter\'s development every day.',
                'is_featured': False,
                'order': 4
            }
        ]

        for data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created testimonial: {testimonial.name}")
            else:
                self.stdout.write(f"- Testimonial already exists: {testimonial.name}")

    def populate_page_sections(self):
        """Populate page sections for various pages"""
        self.stdout.write("\nCreating page sections...")

        sections_data = [
            {
                'section_type': 'about_hero',
                'title': 'About Deigratia Montessori School',
                'subtitle': 'Nurturing Excellence Through Montessori Education',
                'content': 'Discover our commitment to providing quality Montessori education that develops the whole child.',
                'image': 'page_content/deepimg-1743805954179.png'
            },
            {
                'section_type': 'academics_hero',
                'title': 'Academic Excellence',
                'subtitle': 'Comprehensive Montessori Curriculum',
                'content': 'Explore our comprehensive academic programs designed to nurture every child\'s potential.',
                'image': 'page_content/heroimage_1.png'
            },
            {
                'section_type': 'curriculum_image',
                'title': 'Our Learning Environment',
                'subtitle': 'Modern Facilities for Modern Learning',
                'content': 'State-of-the-art facilities that support our innovative teaching methods.',
                'image': 'page_content/deepimg-1743926001836.png'
            }
        ]

        for data in sections_data:
            section, created = PageSection.objects.get_or_create(
                section_type=data['section_type'],
                defaults=data
            )
            if created:
                self.stdout.write(f"✓ Created page section: {section.section_type}")
            else:
                self.stdout.write(f"- Page section already exists: {section.section_type}")
