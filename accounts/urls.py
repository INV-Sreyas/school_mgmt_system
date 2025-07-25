from django.urls import path
from .views import LoginView
# from django.contrib.auth import views as auth_views
# from django.views.decorators.csrf import csrf_exempt
from .views import password_reset_api, reset_password_api

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),

    # path("password_reset/", csrf_exempt(auth_views.PasswordResetView.as_view()), name="password_reset"),
    # path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    
    # path("reset/<uidb64>/<token>/", csrf_exempt(auth_views.PasswordResetConfirmView.as_view()), name="password_reset_confirm"),
    # path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
     path("password_reset/", password_reset_api, name="password_reset_api"),
     path("reset/<uidb64>/<token>/", reset_password_api, name="reset_password_api"),
]
