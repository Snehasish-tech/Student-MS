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

        course_cs, _ = Courses.objects.get_or_create(course_name="BSc Computer Science")
        course_bba, _ = Courses.objects.get_or_create(course_name="BBA")

        staff_users = [
            self._create_staff_user(
                User,
                username="demo_staff_cs",
                email="demo_staff_cs@example.com",
                first_name="Alice",
                last_name="Sharma",
                address="City Center",
            ),
            self._create_staff_user(
                User,
                username="demo_staff_bba",
                email="demo_staff_bba@example.com",
                first_name="Ravi",
                last_name="Verma",
                address="North Avenue",
            ),
        ]

        subjects = [
            self._create_subject("Data Structures", course_cs, staff_users[0]),
            self._create_subject("Database Systems", course_cs, staff_users[0]),
            self._create_subject("Business Management", course_bba, staff_users[1]),
            self._create_subject("Accounting", course_bba, staff_users[1]),
        ]

        students = [
            self._create_student_user(
                User,
                username="demo_student_1",
                email="demo_student_1@example.com",
                first_name="Sneha",
                last_name="Patel",
                gender="Female",
                address="Green Park",
                course=course_cs,
                session_year=session_year,
            ),
            self._create_student_user(
                User,
                username="demo_student_2",
                email="demo_student_2@example.com",
                first_name="Arjun",
                last_name="Nair",
                gender="Male",
                address="Lake Road",
                course=course_cs,
                session_year=session_year,
            ),
            self._create_student_user(
                User,
                username="demo_student_3",
                email="demo_student_3@example.com",
                first_name="Priya",
                last_name="Das",
                gender="Female",
                address="MG Road",
                course=course_cs,
                session_year=session_year,
            ),
            self._create_student_user(
                User,
                username="demo_student_4",
                email="demo_student_4@example.com",
                first_name="Karan",
                last_name="Joshi",
                gender="Male",
                address="River View",
                course=course_bba,
                session_year=session_year,
            ),
            self._create_student_user(
                User,
                username="demo_student_5",
                email="demo_student_5@example.com",
                first_name="Anaya",
                last_name="Singh",
                gender="Female",
                address="Main Street",
                course=course_bba,
                session_year=session_year,
            ),
            self._create_student_user(
                User,
                username="demo_student_6",
                email="demo_student_6@example.com",
                first_name="Rohit",
                last_name="Mehta",
                gender="Male",
                address="Hill Road",
                course=course_bba,
                session_year=session_year,
            ),
        ]

        self._seed_staff_activity(staff_users)
        self._seed_student_activity(students)
        self._seed_attendance_and_results(subjects, students, session_year)

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
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

        AttendanceReport.objects.filter(student_id__admin__in=demo_users).delete()
        AttendanceReport.objects.filter(attendance_id__subject_id__subject_name__in=[
            "Data Structures",
            "Database Systems",
            "Business Management",
            "Accounting",
        ]).delete()

        Attendance.objects.filter(subject_id__subject_name__in=[
            "Data Structures",
            "Database Systems",
            "Business Management",
            "Accounting",
        ]).delete()

        StudentResult.objects.filter(student_id__admin__in=demo_users).delete()
        StudentResult.objects.filter(subject_id__subject_name__in=[
            "Data Structures",
            "Database Systems",
            "Business Management",
            "Accounting",
        ]).delete()

        Students.objects.filter(admin__in=demo_users).delete()
        Staffs.objects.filter(admin__in=demo_users).delete()

        Subjects.objects.filter(subject_name__in=[
            "Data Structures",
            "Database Systems",
            "Business Management",
            "Accounting",
        ]).delete()

        demo_users.delete()