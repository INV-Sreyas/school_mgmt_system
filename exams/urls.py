from django.urls import path
from . import views

urlpatterns = [
    path('exams/create/', views.create_exam),
    path('questions/add/', views.add_question),
    path('exams/', views.list_exams),
    path('student-exam-list/', views.student_exam_list),
    path('student/exam/<int:exam_id>/submission/', views.get_submission_score, name='get_submission_score'),
    path('exams/<int:exam_id>/questions/', views.get_exam_questions),
    path('exams/<int:exam_id>/submit/', views.submit_exam),
]