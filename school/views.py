from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .models import Teacher
from .models import Student
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.utils import is_admin, is_teacher, is_student
from datetime import datetime
import json
import csv
import io
from django.http import HttpResponse
 

# 🔐 Protected View 
# only for testing the access token no need in the functionality at all
class ProtectedTestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello {request.user.username}, you’re authenticated!"})

# ✅ Create Teacher
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_teacher(request):
    data = json.loads(request.body)
    try:
        # 1. Create user
        user = User.objects.create_user(
            username=data['username'],      # Add this field in your request
            password=data['password'],      # Add this field in your request
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        # 2. Add user role
        UserProfile.objects.create(user=user, role='teacher')

        # 3. Create teacher and link to user
        teacher = Teacher.objects.create(
            user=user,  # Make sure your Teacher model has this FK
            phone_number=data['phone_number'],
            subject_specialization=data['subject_specialization'],
            employee_id=data['employee_id'],
            date_of_joining=data['date_of_joining'],
            status=data['status']
        )

        return JsonResponse({'message': 'Teacher created successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# ✅ List Teachers
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_teachers(request):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can perform this action'}, status=403)
    teachers = Teacher.objects.all().values()
    return JsonResponse(list(teachers), safe=False)

# ✅ Update Teacher
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_teacher(request, teacher_id):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can perform this action'}, status=403)
    data = json.loads(request.body)
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        for field in ['first_name', 'last_name', 'email', 'phone_number', 'subject_specialization', 'employee_id', 'date_of_joining', 'status']:
            if field in data:
                setattr(teacher, field, data[field])
        teacher.save()
        return JsonResponse({'message': 'Teacher updated successfully'})
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher not found'}, status=404)

# ✅ Delete Teacher
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_teacher(request, teacher_id):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can perform this action'}, status=403)
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.delete()
        return JsonResponse({'message': 'Teacher deleted successfully'})
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher not found'}, status=404)


# ✅ Create Student
@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_student(request):
    data = json.loads(request.body)
    try:
        # ✅ First create Django User
        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        # ✅ Link the user to UserProfile
        UserProfile.objects.create(user=user, role='student')

        # ✅ Now create the Student
        teacher = Teacher.objects.get(id=data['assigned_teacher'])
        student = Student.objects.create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number'],
            roll_number=data['roll_number'],
            student_class=data['student_class'],
            date_of_birth=data['date_of_birth'],
            admission_date=data['admission_date'],
            status=data['status'],
            assigned_teacher=teacher
        )
        return JsonResponse({'message': 'Student created successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ✅ List Student
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_students(request):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can perform this action'}, status=403)
    students = Student.objects.all().values()
    return JsonResponse(list(students), safe=False)


# ✅ Update Student
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student(request, student_id):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can perform this action'}, status=403)
    data = json.loads(request.body)
    try:
        student = Student.objects.get(id=student_id)
        for field in ['first_name', 'last_name', 'email', 'phone_number', 'roll_number', 'student_class', 'date_of_birth', 'admission_date', 'status']:
            if field in data:
                setattr(student, field, data[field])
        if 'assigned_teacher' in data:
            teacher = Teacher.objects.get(id=data['assigned_teacher'])
            student.assigned_teacher = teacher
        student.save()
        return JsonResponse({'message': 'Student updated successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ✅ Delete Student
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_student(request, student_id):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can perform this action'}, status=403)
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    

# The method for teacher to view their own student
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_assigned_students(request):
    if not is_teacher(request.user):
        return JsonResponse({'error': 'Forbidden: Only teachers allowed'}, status=403)

    try:
        teacher = Teacher.objects.get(user=request.user)
        students = Student.objects.filter(assigned_teacher=teacher).values()
        return JsonResponse(list(students), safe=False)
    except Teacher.DoesNotExist:
        return JsonResponse({'error': 'Teacher profile not found'}, status=404)
    

# The method for student to see their own profile and update fields
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    if not is_student(request.user):
        return JsonResponse({'error': 'Forbidden: Only students can access this'}, status=403)

    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student profile not found'}, status=404)

    if request.method == 'GET':
        data = {
            'first_name': student.first_name,
            'last_name': student.last_name,
            'email': student.email,
            'phone_number': student.phone_number,
            'roll_number': student.roll_number,
            'student_class': student.student_class,
            'date_of_birth': student.date_of_birth,
            'admission_date': student.admission_date,
            'status': student.status,
        }
        return JsonResponse(data)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        for field in ['first_name', 'last_name', 'email', 'phone_number', 'student_class', 'status']:
            if field in data:
                setattr(student, field, data[field])
        student.save()
        return JsonResponse({'message': 'Profile updated successfully'})


# csv export for teacher
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_teachers_csv(request):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can export data'}, status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teachers.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone Number', 'Specialization', 'Employee ID', 'Joining Date', 'Status'])

    for teacher in Teacher.objects.all():
        writer.writerow([
            teacher.id,
            f"{teacher.user.first_name} {teacher.user.last_name}",
            teacher.user.email,
            teacher.phone_number,
            teacher.subject_specialization,
            teacher.employee_id,
            teacher.date_of_joining,
            teacher.status,
        ])

    return response


# csv export for students

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_students_csv(request):
    if not is_admin(request.user):
        return JsonResponse({'error': 'Forbidden: Only admins can export data'}, status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone Number', 'Roll Number', 'Class', 'DOB', 'Admission Date', 'Status', 'Assigned Teacher'])

    for student in Student.objects.all():
        writer.writerow([
            student.id,
            f"{student.user.first_name} {student.user.last_name}",
            student.user.email,
            student.phone_number,
            student.roll_number,
            student.student_class,
            student.date_of_birth,
            student.admission_date,
            student.status,
            student.assigned_teacher.user.get_full_name() if student.assigned_teacher else "",
        ])

    return response


@csrf_exempt
# @login_required
def upload_students_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')

        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Invalid or missing CSV file'}, status=400)

        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            for row in reader :
                Student.objects.create(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    phone_number=row['phone_number'],
                    roll_number=row['roll_number'],
                    student_class=row['student_class'],
                    date_of_birth=datetime.strptime(row['date_of_birth'], "%Y-%m-%d").date(),
                    admission_date=datetime.strptime(row['admission_date'], "%Y-%m-%d").date(),
                    status=row['status'],
                    assigned_teacher=Teacher.objects.filter(id=row['assigned_teacher_id']).first()  # safe FK handling
                )

            return JsonResponse({'message': 'Students uploaded successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Upload failed: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only POST allowed'}, status=405)