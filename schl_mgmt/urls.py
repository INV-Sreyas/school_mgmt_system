"""
URL configuration for schl_mgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from school.views import (
    ProtectedTestView,
    create_teacher,
    list_teachers,
    update_teacher,
    delete_teacher,
    create_student,
    list_students,
    update_student,
    delete_student
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/school/", include("school.urls")),
    path('protected/', ProtectedTestView.as_view()),
    path('teachers/', list_teachers),
    path('teachers/create/', create_teacher),
    path('teachers/update/<int:teacher_id>/', update_teacher),
    path('teachers/delete/<int:teacher_id>/', delete_teacher),
    path("students/create/", create_student),
    path("students/", list_students),
    path("students/update/<int:student_id>/", update_student),
    path("students/delete/<int:student_id>/", delete_student),
]
