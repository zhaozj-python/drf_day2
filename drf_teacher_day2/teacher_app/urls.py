from django.urls import path

from teacher_app import views

urlpatterns = [
    path("teacher/", views.TeacherAPIView.as_view()),
    path("teacher/<str:id>/", views.TeacherAPIView.as_view()),
    path("teachergen/", views.TeacherGenericAPIView.as_view()),
    path("teachergen/<str:id>/", views.TeacherGenericAPIView.as_view()),
]