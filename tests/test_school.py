import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from accounts.models import UserProfile
from school.models import Teacher, Student
from datetime import date


class SchoolViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create admin user
        self.admin_user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        UserProfile.objects.create(user=self.admin_user, role='admin')
        self.client.force_authenticate(user=self.admin_user)

        # Create teacher user
        self.teacher_user = User.objects.create_user(username='teacher1', password='pass123')
        UserProfile.objects.create(user=self.teacher_user, role='teacher')
        self.teacher = Teacher.objects.create(
            user=self.teacher_user,
            phone_number='1234567890',
            subject_specialization='Maths',
            employee_id='T001',
            date_of_joining='2023-01-01',
            status='active'
        )

        # Create student user
        self.student_user = User.objects.create_user(username='student1', password='pass123')
        UserProfile.objects.create(user=self.student_user, role='student')
        self.student = Student.objects.create(
            user=self.student_user,
            first_name='Stu',
            last_name='Dent',
            email='student@example.com',
            phone_number='9876543210',
            roll_number='R001',
            student_class='10A',
            date_of_birth='2008-05-10',
            admission_date='2024-06-01',
            status='active',
            assigned_teacher=self.teacher
        )

    def test_create_teacher(self):
        payload = {
            "username": "teacher2",
            "password": "pass123",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com",
            "phone_number": "9999999999",
            "subject_specialization": "Science",
            "employee_id": "T002",
            "date_of_joining": "2023-01-01",
            "status": "active"
        }
        response = self.client.post("/api/school/teachers/create/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_list_teachers(self):
        response = self.client.get("/api/school/teachers/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)

    def test_update_teacher(self):
        response = self.client.put(f"/api/school/teachers/update/{self.teacher.id}/", data=json.dumps({"status": "inactive"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.status, 'inactive')

    def test_delete_teacher(self):
        response = self.client.delete(f"/api/school/teachers/delete/{self.teacher.id}/")
        self.assertEqual(response.status_code, 200)

    def test_create_student(self):
        payload = {
            "username": "student2",
            "password": "pass123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone_number": "9998887776",
            "roll_number": "R002",
            "student_class": "9A",
            "date_of_birth": "2009-03-04",
            "admission_date": "2024-06-05",
            "status": "active",
            "assigned_teacher": self.teacher.id
        }
        response = self.client.post("/api/school/students/create/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_list_students(self):
        response = self.client.get("/api/school/students/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()) >= 1)

    def test_update_student(self):
        response = self.client.put(f"/api/school/students/update/{self.student.id}/", data=json.dumps({"status": "inactive"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.status, 'inactive')

    def test_delete_student(self):
        response = self.client.delete(f"/api/school/students/delete/{self.student.id}/")
        self.assertEqual(response.status_code, 200)

    def test_export_teachers_csv(self):
        response = self.client.get("/api/school/export/teachers/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response['Content-Type'])

    def test_export_students_csv(self):
        response = self.client.get("/api/school/export/students/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/csv", response['Content-Type'])
    