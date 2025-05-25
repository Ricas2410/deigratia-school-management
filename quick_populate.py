import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ricas_school_manager.settings')
django.setup()

from website.models import HeroSlide, GalleryImage, StaffMember

def create_hero_slides():
    print("Creating hero slides...")
    
    # Clear existing slides
    HeroSlide.objects.all().delete()
    
    slides = [
        {
            'title': 'Welcome to Deigratia Montessori School',
            'subtitle': 'Nurturing Excellence Through Montessori Education',
            'image': 'hero_slides/Cultural_Dance_at_Montessori_school_in_Ghana.png',
            'order': 1,
            'is_active': True
        },
        {
            'title': 'Modern Learning Environment',
            'subtitle': 'State-of-the-art computer lab for digital literacy',
            'image': 'hero_slides/Montessori_school_computer_lab_in_Ghana_1.png',
            'order': 2,
            'is_active': True
        },
        {
            'title': 'STEM Education Excellence',
            'subtitle': 'Hands-on robotics and technology learning',
            'image': 'hero_slides/Montessori_school_robotics_class_in_Ghana.png',
            'order': 3,
            'is_active': True
        },
        {
            'title': 'Inspiring Young Minds',
            'subtitle': 'Creating tomorrow\'s leaders through quality education',
            'image': 'hero_slides/youn-girl_in-class.png',
            'order': 4,
            'is_active': True
        },
        {
            'title': 'Bright Futures Start Here',
            'subtitle': 'Where every child\'s potential is nurtured and celebrated',
            'image': 'hero_slides/sunshine_hero.png',
            'order': 5,
            'is_active': True
        }
    ]
    
    for slide_data in slides:
        slide = HeroSlide.objects.create(**slide_data)
        print(f"✓ Created: {slide.title}")

def create_gallery():
    print("\nCreating gallery images...")
    
    # Clear existing gallery
    GalleryImage.objects.all().delete()
    
    gallery = [
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
        }
    ]
    
    for img_data in gallery:
        img = GalleryImage.objects.create(**img_data)
        print(f"✓ Created: {img.title}")

def create_staff():
    print("\nCreating staff members...")
    
    # Clear existing staff
    StaffMember.objects.all().delete()
    
    staff = [
        {
            'name': 'Dr. Kwame Nkrumah',
            'position': 'School Director',
            'bio': 'Dr. Nkrumah brings over 20 years of experience in Montessori education. He holds a PhD in Educational Leadership and is passionate about creating nurturing learning environments for children.',
            'image': 'staff/Kwame-Nkrumah-1024x1024.jpg',
            'email': 'director@deigratiamontessori.edu',
            'phone': '+233 24 123 4567',
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
            'is_featured': False,
            'order': 4
        }
    ]
    
    for staff_data in staff:
        member = StaffMember.objects.create(**staff_data)
        print(f"✓ Created: {member.name}")

if __name__ == '__main__':
    print("🚀 Populating website with your images...")
    print("=" * 50)
    
    try:
        create_hero_slides()
        create_gallery()
        create_staff()
        
        print("\n" + "=" * 50)
        print("✅ SUCCESS! Your images are now being used on the website!")
        print(f"- {HeroSlide.objects.count()} Hero slides created")
        print(f"- {GalleryImage.objects.count()} Gallery images created")
        print(f"- {StaffMember.objects.count()} Staff members created")
        print("\n🌟 Visit your website to see the changes!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
