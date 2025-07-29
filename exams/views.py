from django.shortcuts import render
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from .models import Exam
from .models import Question, Exam



@csrf_exempt
@login_required
def create_exam(request):
    if request.method == 'POST':
        user = request.user
        if user.userprofile.role != "teacher":
            return JsonResponse({"error": "Only teachers can create exams."}, status=403)

        data = json.loads(request.body)
        title = data.get("title")
        subject = data.get("subject")

        if not title or not subject:
            return JsonResponse({"error": "Title and subject required."}, status=400)

        exam = Exam.objects.create(
            teacher=user,
            title=title,
            subject=subject,
        )
        return JsonResponse({"message": "Exam created.", "exam_id": exam.id})



@csrf_exempt
@login_required
def add_question(request):
    if request.method == 'POST':
        user = request.user
        if user.userprofile.role != "teacher":
            return JsonResponse({"error": "Only teachers can add questions."}, status=403)

        data = json.loads(request.body)
        exam_id = data.get("exam_id")

        try:
            exam = Exam.objects.get(id=exam_id, teacher=user)
        except Exam.DoesNotExist:
            return JsonResponse({"error": "Exam not found or unauthorized."}, status=404)

        question = Question.objects.create(
            exam=exam,
            text=data.get("text"),
            option1=data.get("option1"),
            option2=data.get("option2"),
            option3=data.get("option3"),
            option4=data.get("option4"),
            correct_option=data.get("correct_option")
        )

        return JsonResponse({"message": "Question added.", "question_id": question.id})



@login_required
def list_exams(request):
    if request.method == 'GET':
        exams = Exam.objects.all().values('id', 'title', 'subject', 'date_created')
        return JsonResponse(list(exams), safe=False)


@login_required
def student_exam_list(request):
    if request.user.userprofile.role != "student":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    exams = Exam.objects.all().values("id", "title", "subject")
    return JsonResponse(list(exams), safe=False)


@login_required
def get_exam_questions(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return JsonResponse({"error": "Exam not found"}, status=404)

    questions = exam.questions.all().values(
        'id', 'text', 'option1', 'option2', 'option3', 'option4'
    )
    return JsonResponse(list(questions), safe=False)


from .models import StudentExamSubmission, Answer, Question


@csrf_exempt
@login_required
def submit_exam(request, exam_id):
    if request.method == 'POST':
        user = request.user
        if user.userprofile.role != "student":
            return JsonResponse({"error": "Only students can submit exams."}, status=403)

        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            return JsonResponse({"error": "Exam not found"}, status=404)

        if StudentExamSubmission.objects.filter(student=user, exam=exam).exists():
            return JsonResponse({"error": "You have already submitted this exam."}, status=400)

        data = json.loads(request.body)
        answers = data.get("answers", [])  # List of {"question_id": int, "selected_option": "option1"}

        submission = StudentExamSubmission.objects.create(student=user, exam=exam)

        correct = 0
        for ans in answers:
            try:
                question = Question.objects.get(id=ans["question_id"], exam=exam)
                selected = ans["selected_option"]
                Answer.objects.create(submission=submission, question=question, selected_option=selected)
                if selected == question.correct_option:
                    correct += 1
            except:
                continue

        total = exam.questions.count()
        score = (correct / total) * 100 if total > 0 else 0
        submission.score = score
        submission.save()

        return JsonResponse({"message": "Exam submitted", "score": score})
    

@login_required
def get_submission_score(request, exam_id):
    user = request.user
    try:
        submission = StudentExamSubmission.objects.get(student=user, exam__id=exam_id)
        return JsonResponse({"score": submission.score})
    except StudentExamSubmission.DoesNotExist:
        return JsonResponse({"error": "Submission not found."}, status=404)

