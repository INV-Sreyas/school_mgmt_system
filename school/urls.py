from django.urls import path
from .views import ProtectedTestView, create_teacher, create_student, list_students, update_student, delete_student  # make sure create_teacher is imported

urlpatterns = [
    path("protected/", ProtectedTestView.as_view(), name="protected"),
    path("teachers/create/", create_teacher, name="create-teacher"),
    path("students/create/", create_student),
    path("students/", list_students),
    path("students/update/<int:student_id>/", update_student),
    path("students/delete/<int:student_id>/", delete_student),

]

