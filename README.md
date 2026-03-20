# Student Management System (SMS) 🎓

[![Django](https://img.shields.io/badge/Django-5.2.12-green)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

## 📖 Overview

A comprehensive, enterprise-grade Student Management System built with **Django 5.2.12**. SMS is designed to streamline and automate academic operations for educational institutions, colleges, and universities. The platform provides secure, role-based access for Administrators, Faculty Members, and Students, facilitating efficient management of admissions, attendance, results, and institutional operations.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [User Roles & Permissions](#-user-roles--permissions)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#️-installation--setup)
- [Configuration](#-configuration)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)
- [Support](#-support)

---

## 🖼️ Screenshots

<p align="center">
  
  <img width="1822" height="919" alt="Screenshot 2026-03-20 113027" src="https://github.com/user-attachments/assets/71a669a9-37f3-401b-8a64-6ddf4c8e1874" />
<img width="1761" height="903" alt="Screenshot 2026-03-20 113604" src="https://github.com/user-attachments/assets/a61bbb0e-e470-4cd5-bd38-c7964d850d56" />

</p>


---

## ✨ Features

### Administrative Features
- 📊 **Comprehensive Dashboard:** Real-time analytics and institution overview
- 👥 **Staff Management:** Add, update, and manage faculty members
- 🎓 **Student Management:** Complete student lifecycle management
- 📚 **Course Management:** Create and organize academic courses
- 🗓️ **Session Management:** Manage academic sessions and schedules
- 📋 **Subject Management:** Organize subjects and course mappings
- 📝 **System Configuration:** Settings and global configurations

### Staff Portal Features
- ✅ **Attendance Management:** Mark and track student attendance
- 📊 **Results Management:** Update and publish student grades
- 🏥 **Leave Requests:** View and manage leave applications
- 📈 **Performance Analytics:** View class-wise performance metrics
- 📱 **Notifications:** Instant alerts for important events

### Student Portal Features
- 📋 **Attendance Tracking:** View personal attendance records
- 📊 **Results & Grades:** Check academic performance
- 🏥 **Leave Applications:** Submit and track leave requests
- 📢 **Announcements:** Stay updated with institutional news
- 📧 **Communication:** Contact faculty and administration

### Technical Features
- 🎨 **Modern UI/UX:** Glass-morphism design with responsive layout
- 🔐 **Role-Based Access Control (RBAC):** Secure permission system
- 📱 **Fully Responsive:** Desktop, tablet, and mobile compatible
- 🚀 **Performance Optimized:** Fast load times and smooth interactions
- 🔄 **Real-time Updates:** Live attendance and result tracking
- 🌙 **Dark Mode Support:** Professional dark theme
- ♿ **Accessibility Compliant:** WCAG 2.1 standards

---

## 🚀 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 5.2.12 |
| **Programming Language** | Python 3.9+ |
| **Database (Dev)** | SQLite3 |
| **Database (Prod)** | PostgreSQL 12+ |
| **Frontend** | HTML5, CSS3 (Flexbox/Grid) |
| **Scripting** | JavaScript (ES6+) |
| **UI Libraries** | Google Fonts (Syne, DM Sans) |
| **Styling** | Glass-morphism, Custom Animations |
| **Static Files** | Whitenoise |
| **Deployment** | Vercel |
| **Version Control** | Git |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Client (Browser)                    │
│                    (HTML5, CSS3, JS)                    │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
         ┌────▼────┐          ┌────▼─────┐
         │ Static  │          │ Templates │
         │ Files   │          │ (Django)  │
         └─────────┘          └────┬──────┘
                                   │
┌──────────────────────────────────┴──────────────────────────┐
│                    Django Application                       │
│  ┌───────────────┐  ┌──────────┐  ┌─────────────────────┐  │
│  │   Views       │  │  Models  │  │  Forms & Validation │  │
│  │ (HodViews,    │  │ (Student,│  │                     │  │
│  │  StaffViews,  │  │  Staff,  │  │                     │  │
│  │  StudentViews)│  │  etc.)   │  │                     │  │
│  └───────────────┘  └──────────┘  └─────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             Authentication & Permissions               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────┬────────────────────────────────────┘
                          │
                    ┌─────▼──────┐
                    │  Database  │
                    │  (SQLite / │
                    │ PostgreSQL)│
                    └────────────┘
```

---

## 👥 User Roles & Permissions

| Role | Dashboard | Staff Mgmt | Student Mgmt | Attendance | Results | Leave Requests |
|------|-----------|-----------|-------------|-----------|---------|----------------|
| **Admin (HOD)** | ✅ Full | ✅ Full CRUD | ✅ Full CRUD | ✅ View | ✅ View | ✅ Approve/Reject |
| **Staff (Faculty)** | ✅ Limited | ❌ None | ❌ None | ✅ Mark/Update | ✅ Publish | ❌ Submit Only |
| **Student** | ✅ User Profile | ❌ None | ❌ None | ✅ View Only | ✅ View Only | ✅ Submit |

---

## 📋 Prerequisites

Before installation, ensure you have the following:

- **Python:** 3.9 or higher
- **pip:** Python package manager
- **Git:** Version control (optional but recommended)
- **Virtual Environment:** Recommended for isolation
- **Database:** SQLite (included) or PostgreSQL for production

Check your versions:
```bash
python --version
pip --version
git --version
```

---

## 🛠️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Snehasish-tech/Student-MS.git
cd Student-MS
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# (Database credentials, secret key, etc.)
```

### Step 5: Database Setup
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Load sample data (optional)
python manage.py seed_demo_data
```

### Step 6: Create Admin Account
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin credentials.

### Step 7: Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```ini
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Django Settings (`student_management_project/settings.py`)

Key configurations:
- **INSTALLED_APPS:** Django apps and third-party packages
- **MIDDLEWARE:** Request processing chain
- **DATABASES:** Database configuration
- **STATIC_FILES:** Static files configuration
- **TEMPLATES:** Template engine settings

---

## 📊 Database Schema

### Key Models

```
Student
  ├── id (Primary Key)
  ├── admin (ForeignKey: User)
  ├── roll_number (Unique)
  ├── first_name
  ├── last_name
  ├── sex
  ├── date_of_birth
  ├── session (ForeignKey: Session)
  └── created_at

Staff
  ├── id (Primary Key)
  ├── admin (ForeignKey: User)
  ├── full_name
  ├── sex
  ├── date_of_birth
  ├── assigned_date
  └── created_at

Course
  ├── id (Primary Key)
  ├── course_name (Unique)
  └── created_at

Session
  ├── id (Primary Key)
  ├── session_year_start
  ├── session_year_end
  └── created_at

Subject
  ├── id (Primary Key)
  ├── subject_name
  ├── course (ForeignKey: Course)
  ├── staff (ForeignKey: Staff)
  └── created_at

Attendance
  ├── id (Primary Key)
  ├── student (ForeignKey: Student)
  ├── subject (ForeignKey: Subject)
  ├── attendance_date
  ├── status (Present/Absent)
  └── created_at

StudentResult
  ├── id (Primary Key)
  ├── student (ForeignKey: Student)
  ├── subject (ForeignKey: Subject)
  ├── marks
  ├── grade
  └── created_at
```

---

## 📡 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /logout` - User logout
- `POST /registration` - New user registration

### Admin Endpoints
- `GET /admin/home` - Admin dashboard
- `GET /admin/view-staff` - List all staff
- `POST /admin/add-staff` - Add new staff member
- `GET /admin/view-students` - List all students
- `POST /admin/add-student` - Add new student

### Staff Endpoints
- `GET /staff/home` - Staff dashboard
- `POST /staff/mark-attendance` - Mark student attendance
- `POST /staff/submit-results` - Publish student results

### Student Endpoints
- `GET /student/home` - Student dashboard
- `GET /student/view-attendance` - View attendance records
- `GET /student/view-results` - View grades and results

---

## 📦 Deployment

### Vercel Deployment

The project is pre-configured for Vercel:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deployment ready"
   git push origin main
   ```

2. **Connect to Vercel:**
   - Visit [Vercel Dashboard](https://vercel.com/dashboard)
   - Import GitHub repository
   - Configure environment variables
   - Deploy

3. **Production Database:**
   - Use PostgreSQL for production
   - Update `settings.py` with production database credentials

4. **Static Files:**
   - Whitenoise handles static file serving
   - No additional configuration needed

---

## 🔧 Troubleshooting

### Common Issues & Solutions

**Issue 1: `ModuleNotFoundError`**
```bash
# Solution: Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

**Issue 2: Database Migration Errors**
```bash
# Solution: Reset migrations (development only)
python manage.py migrate student_management_app zero
python manage.py migrate
```

**Issue 3: Static Files Not Loading**
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

**Issue 4: SuperUser Creation Fails**
```bash
# Solution: Reset database and recreate
python manage.py flush
python manage.py createsuperuser
```

**Issue 5: Port 8000 Already in Use**
```bash
# Solution: Specify different port
python manage.py runserver 8001
```

---

## 🤝 Contributing

We welcome contributions from the community!

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/AmazingFeature`
3. **Commit** changes: `git commit -m 'Add AmazingFeature'`
4. **Push** to branch: `git push origin feature/AmazingFeature`
5. **Submit** a Pull Request

### Contribution Guidelines
- Follow PEP 8 for Python code
- Add comments for complex logic
- Update documentation for new features
- Test changes before submitting

---

## 🗓️ Roadmap

### Upcoming Features
- [ ] SMS/Email notifications
- [ ] Advanced analytics and reporting
- [ ] Mobile app (React Native)
- [ ] AI-powered performance predictions
- [ ] Multi-language support
- [ ] Video conferencing integration
- [ ] Digital assignment submission
- [ ] Parent portal

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by TEAM PLUTO
  <br>
  <strong>Student Management System (SMS)</strong> © 2026
</p>
