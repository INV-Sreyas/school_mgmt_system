from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject}"


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=10)  # e.g., "option1"

    def __str__(self):
        return f"{self.text[:50]}..."


class StudentExamSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"


class Answer(models.Model):
    submission = models.ForeignKey(StudentExamSubmission, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=10)  # e.g., "option2"

    def __str__(self):
        return f"{self.question.id} - {self.selected_option}"
