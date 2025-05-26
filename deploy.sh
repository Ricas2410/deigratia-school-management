#!/bin/bash

# PythonAnywhere Deployment Script for Deigratia School Management System
# Run this script after cloning the repository on PythonAnywhere

echo "🚀 Starting deployment of Deigratia School Management System..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root directory."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.10 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration before continuing."
    echo "   nano .env"
    read -p "Press Enter after editing .env file..."
fi

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser..."
echo "You can skip this if you already have a superuser account."
python manage.py createsuperuser

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create media directories
echo "📂 Creating media directories..."
mkdir -p media/profile_pics
mkdir -p media/course_materials
mkdir -p media/assignments
mkdir -p media/gallery
mkdir -p media/hero_slides
mkdir -p media/announcements
mkdir -p media/events

# Set permissions
echo "🔐 Setting permissions..."
chmod -R 755 media/
chmod -R 755 staticfiles/

# Test the installation
echo "🧪 Testing installation..."
python manage.py check

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your web app in PythonAnywhere:"
echo "   - Source code: /home/deigratiams/deigratia-school-management"
echo "   - Virtualenv: /home/deigratiams/deigratia-school-management/venv"
echo "   - WSGI file: Update with the provided configuration"
echo ""
echo "2. Configure static files mapping:"
echo "   - URL: /static/"
echo "   - Directory: /home/deigratiams/deigratia-school-management/staticfiles/"
echo ""
echo "3. Configure media files mapping:"
echo "   - URL: /media/"
echo "   - Directory: /home/deigratiams/deigratia-school-management/media/"
echo ""
echo "4. Reload your web app"
echo ""
echo "🎓 Your school management system is ready!"
