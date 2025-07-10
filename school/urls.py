from django.urls import path
from .views import (ProtectedTestView,list_teachers, create_teacher,update_teacher,
                    delete_teacher, create_student, list_students, update_student, 
                    delete_student, list_assigned_students, student_profile)

urlpatterns = [
    path("protected/", ProtectedTestView.as_view(), name="protected"),
     path('teachers/', list_teachers),
    path("teachers/create/", create_teacher, name="create-teacher"),
    path('teachers/update/<int:teacher_id>/', update_teacher),
    path('teachers/delete/<int:teacher_id>/', delete_teacher),
    path("students/create/", create_student),
    path("students/", list_students),
    path("students/update/<int:student_id>/", update_student),
    path("students/delete/<int:student_id>/", delete_student),
    path("teacher/students/", list_assigned_students, name="assigned-students"),
    path("student/profile/", student_profile, name="student-profile"),

]

