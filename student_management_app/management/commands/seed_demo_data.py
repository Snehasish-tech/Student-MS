import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from student_management_app.models import (
    AdminHOD,
    Attendance,
    AttendanceReport,
    Courses,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    SessionYearModel,
    Staffs,
    StudentResult,
    Students,
    Subjects,
)


class Command(BaseCommand):
    help = "Seed demo data for staff, courses, students, subjects, and attendance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete old demo data (demo_*) before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        if options["reset"]:
            self._reset_demo_data(User)

        self._create_hod_user(User)

        session_year, _ = SessionYearModel.objects.get_or_create(
            session_start_year=date(2025, 4, 1),
            session_end_year=date(2026, 3, 31),
        )

        course_names = [
            "BSc Computer Science",
            "BCA",
            "BBA",
            "BCom",
            "BA English",
            "BSc Mathematics",
            "BSc Physics",
            "BSc Chemistry",
        ]
        courses = {
            name: Courses.objects.get_or_create(course_name=name)[0]
            for name in course_names
        }

        staff_specs = [
            ("demo_staff_cs", "Alice", "Sharma", "City Center", "BSc Computer Science"),
            ("demo_staff_bca", "Rahul", "Verma", "North Avenue", "BCA"),
            ("demo_staff_bba", "Ravi", "Nair", "South Block", "BBA"),
            ("demo_staff_bcom", "Neha", "Kapoor", "Lake Town", "BCom"),
            ("demo_staff_eng", "Ishita", "Roy", "Green View", "BA English"),
            ("demo_staff_math", "Sourav", "Dutta", "Hill Road", "BSc Mathematics"),
            ("demo_staff_phy", "Ankit", "Das", "Riverside", "BSc Physics"),
            ("demo_staff_chem", "Priyanshi", "Mehra", "Sunrise Park", "BSc Chemistry"),
        ]
        staff_users = []
        staff_by_course = {}
        for username, first_name, last_name, address, course_name in staff_specs:
            staff_user = self._create_staff_user(
                User,
                username=username,
                email=f"{username}@example.com",
                first_name=first_name,
                last_name=last_name,
                address=address,
            )
            staff_users.append(staff_user)
            staff_by_course[course_name] = staff_user

        subject_plan = {
            "BSc Computer Science": ["Data Structures", "Database Systems", "Operating Systems"],
            "BCA": ["Programming in C", "Web Technologies", "Computer Networks"],
            "BBA": ["Business Management", "Marketing", "Human Resources"],
            "BCom": ["Accounting", "Corporate Finance", "Business Law"],
            "BA English": ["Literary Theory", "Poetry", "Communication Skills"],
            "BSc Mathematics": ["Algebra", "Calculus", "Statistics"],
            "BSc Physics": ["Mechanics", "Electromagnetism", "Quantum Physics"],
            "BSc Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry"],
        }

        subjects = []
        for course_name, subject_names in subject_plan.items():
            for subject_name in subject_names:
                subjects.append(
                    self._create_subject(subject_name, courses[course_name], staff_by_course[course_name])
                )

        first_names = [
            "Sneha", "Arjun", "Priya", "Karan", "Anaya", "Rohit", "Aditi", "Vivek", "Pooja", "Naman",
            "Riya", "Aman", "Meera", "Sagnik", "Diya", "Harsh", "Tanisha", "Yash", "Simran", "Ayaan",
        ]
        last_names = [
            "Patel", "Nair", "Das", "Joshi", "Singh", "Mehta", "Roy", "Dutta", "Khan", "Ghosh",
            "Mukherjee", "Sharma", "Verma", "Reddy", "Saha", "Mitra", "Bose", "Chopra", "Kapoor", "Paul",
        ]

        students = []
        student_index = 1
        for course_name in course_names:
            for _ in range(10):
                fname = first_names[(student_index - 1) % len(first_names)]
                lname = last_names[(student_index - 1) % len(last_names)]
                gender = "Female" if student_index % 2 else "Male"
                students.append(
                    self._create_student_user(
                        User,
                        username=f"demo_student_{student_index:03d}",
                        email=f"demo_student_{student_index:03d}@example.com",
                        first_name=fname,
                        last_name=lname,
                        gender=gender,
                        address=f"Demo Address {student_index}",
                        course=courses[course_name],
                        session_year=session_year,
                    )
                )
                student_index += 1

        # Backward-compatible demo usernames used in previous test flows.
        for legacy_id in range(1, 7):
            self._create_student_user(
                User,
                username=f"demo_student_{legacy_id}",
                email=f"demo_student_{legacy_id}@example.com",
                first_name=first_names[(legacy_id - 1) % len(first_names)],
                last_name=last_names[(legacy_id - 1) % len(last_names)],
                gender="Female" if legacy_id % 2 else "Male",
                address=f"Legacy Demo Address {legacy_id}",
                course=courses["BSc Computer Science"],
                session_year=session_year,
            )

        self._seed_staff_activity(staff_users)
        self._seed_student_activity(students)
        self._seed_attendance_and_results(subjects, students, session_year)

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write(
            f"Courses: {len(course_names)} | Staff: {len(staff_users)} | Subjects: {len(subjects)} | Students: {len(students)}"
        )
        self.stdout.write("Demo password for all users: demo1234")

    def _create_staff_user(self, User, username, email, first_name, last_name, address):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "user_type": "2",
            },
        )
        if created:
            user.set_password("demo1234")
            user.save()

        staff, _ = Staffs.objects.get_or_create(admin=user)
        staff.address = address
        staff.save()
        return user

    def _create_hod_user(self, User):
        hod_user, created = User.objects.get_or_create(
            username="demo_hod",
            defaults={
                "email": "demo_hod@example.com",
                "first_name": "Head",
                "last_name": "Admin",
                "user_type": "1",
            },
        )
        if created:
            hod_user.set_password("demo1234")
            hod_user.save()

        AdminHOD.objects.get_or_create(admin=hod_user)
        return hod_user

    def _create_student_user(
        self,
        User,
        username,
        email,
        first_name,
        last_name,
        gender,
        address,
        course,
        session_year,
    ):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "user_type": "3",
            },
        )
        if created:
            user.set_password("demo1234")
            user.save()

        student, _ = Students.objects.get_or_create(admin=user)
        student.gender = gender
        student.address = address
        student.course_id = course
        student.session_year_id = session_year
        student.save()
        return student

    def _create_subject(self, name, course, staff_user):
        subject, _ = Subjects.objects.get_or_create(
            subject_name=name,
            course_id=course,
            staff_id=staff_user,
        )
        return subject

    def _seed_attendance_and_results(self, subjects, students, session_year):
        # Create attendance records for the past 45 days (covering ~9 weeks)
        demo_dates = [date.today() - timedelta(days=i) for i in range(1, 45)]

        for subject in subjects:
            subject_students = [s for s in students if s.course_id_id == subject.course_id_id]
            
            # Attendance records
            for day in demo_dates:
                attendance, _ = Attendance.objects.get_or_create(
                    subject_id=subject,
                    attendance_date=day,
                    session_year_id=session_year,
                )

                for student in subject_students:
                    # 80% present, 20% absent (realistic pattern)
                    AttendanceReport.objects.get_or_create(
                        student_id=student,
                        attendance_id=attendance,
                        defaults={"status": random.random() < 0.8},
                    )

            # Results (with varied marks for realistic distribution)
            for student in subject_students:
                StudentResult.objects.get_or_create(
                    student_id=student,
                    subject_id=subject,
                    defaults={
                        "subject_exam_marks": random.randint(50, 98),
                        "subject_assignment_marks": random.randint(8, 25),
                    },
                )

    def _seed_student_activity(self, students):
        for idx, student in enumerate(students, start=1):
            FeedBackStudent.objects.create(
                student_id=student,
                feedback=f"Demo feedback from student {idx}: Need more revision sessions for upcoming exams.",
                feedback_reply="We will schedule one weekly revision class.",
            )
            FeedBackStudent.objects.create(
                student_id=student,
                feedback=f"Demo feedback from student {idx}: Please share assignment rubrics early.",
                feedback_reply="",
            )

            LeaveReportStudent.objects.create(
                student_id=student,
                leave_date=str(date.today() - timedelta(days=6)),
                leave_message="Demo sick leave request",
                leave_status=1,
            )
            LeaveReportStudent.objects.create(
                student_id=student,
                leave_date=str(date.today() + timedelta(days=2)),
                leave_message="Demo personal work leave request",
                leave_status=0,
            )

    def _seed_staff_activity(self, staff_users):
        for idx, staff_user in enumerate(staff_users, start=1):
            staff_obj = Staffs.objects.get(admin=staff_user)

            FeedBackStaffs.objects.create(
                staff_id=staff_obj,
                feedback=f"Demo staff feedback {idx}: Please add more lab equipment.",
                feedback_reply="Request submitted to procurement team.",
            )
            FeedBackStaffs.objects.create(
                staff_id=staff_obj,
                feedback=f"Demo staff feedback {idx}: Need a timetable adjustment for section B.",
                feedback_reply="",
            )

            LeaveReportStaff.objects.create(
                staff_id=staff_obj,
                leave_date=str(date.today() - timedelta(days=5)),
                leave_message="Demo staff medical leave",
                leave_status=1,
            )
            LeaveReportStaff.objects.create(
                staff_id=staff_obj,
                leave_date=str(date.today() + timedelta(days=3)),
                leave_message="Demo staff personal leave",
                leave_status=0,
            )

    def _reset_demo_data(self, User):
        demo_users = User.objects.filter(username__startswith="demo_")
        demo_subjects = Subjects.objects.filter(staff_id__in=demo_users)

        FeedBackStudent.objects.filter(student_id__admin__in=demo_users).delete()
        FeedBackStaffs.objects.filter(staff_id__admin__in=demo_users).delete()
        LeaveReportStudent.objects.filter(student_id__admin__in=demo_users).delete()
        LeaveReportStaff.objects.filter(staff_id__admin__in=demo_users).delete()

        AttendanceReport.objects.filter(student_id__admin__in=demo_users).delete()
        AttendanceReport.objects.filter(attendance_id__subject_id__in=demo_subjects).delete()

        Attendance.objects.filter(subject_id__in=demo_subjects).delete()

        StudentResult.objects.filter(student_id__admin__in=demo_users).delete()
        StudentResult.objects.filter(subject_id__in=demo_subjects).delete()

        Students.objects.filter(admin__in=demo_users).delete()
        Staffs.objects.filter(admin__in=demo_users).delete()
        AdminHOD.objects.filter(admin__in=demo_users).delete()

        demo_subjects.delete()

        demo_users.delete()