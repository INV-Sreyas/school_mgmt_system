from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
import json

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            role = user.userprofile.role
            return Response({
                "message": "Login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "role" : role
            })
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)




@csrf_exempt
def password_reset_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)

    User = get_user_model()
    users = User.objects.filter(email=email)
    if not users.exists():
        return JsonResponse({"message": "If an account exists, you'll receive an email shortly."})  # No info leak

    for user in users:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
        subject = "Reset your password"
        message = f"Click the link to reset your password: {reset_link}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return JsonResponse({"message": "Password reset email sent if user exists."})





@csrf_exempt
def reset_password_api(request, uidb64, token):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        password = data.get("password")
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not password:
        return JsonResponse({"error": "Password is required"}, status=400)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return JsonResponse({"error": "Invalid user"}, status=400)

    if not default_token_generator.check_token(user, token):
        return JsonResponse({"error": "Invalid or expired token"}, status=400)

    user.set_password(password)
    user.save()
    return JsonResponse({"message": "Password has been reset successfully."})