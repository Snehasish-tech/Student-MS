"""
Vercel Serverless Function Handler for Django
This file serves as the entry point for Vercel's serverless platform.
"""

import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management_project.settings')

# Import and configure Django
import django
django.setup()

# Import the WSGI application
from student_management_project.wsgi import application

# Export for Vercel
app = application
