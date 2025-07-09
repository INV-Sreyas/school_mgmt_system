from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .models import Teacher
from .models import Student
import json

# 🔐 Protected View (already present)
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
        teacher = Teacher.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
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
    teachers = Teacher.objects.all().values()
    return JsonResponse(list(teachers), safe=False)

# ✅ Update Teacher
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_teacher(request, teacher_id):
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
        teacher = Teacher.objects.get(id=data['assigned_teacher']) if data.get('assigned_teacher') else None
        student = Student.objects.create(
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
    students = Student.objects.all().values()
    return JsonResponse(list(students), safe=False)


# ✅ Update Student
@csrf_exempt
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student(request, student_id):
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
    try:
        student = Student.objects.get(id=student_id)
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)