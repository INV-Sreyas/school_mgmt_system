from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    subject_specialization = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_joining = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Student(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    roll_number = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    admission_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    assigned_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
