from django.urls import path

from teacher_app import views

urlpatterns = [
    path("teacher/", views.TeacherAPIView.as_view()),
    path("teacher/<str:id>/", views.TeacherAPIView.as_view()),
    path("teachergen/", views.TeacherGenericAPIView.as_view()),
    path("teachergen/<str:id>/", views.TeacherGenericAPIView.as_view()),
    path("user/login/", views.UserViewSetView.as_view({"post": "user_login", "get": "get_user_count"})),
    # path("user/login/<str:id>/", views.UserViewSetView.as_view({"post": "user_login", "get": "get_user_count"})),
    path("user/register/", views.UserREGViewSetView.as_view({"post": "user_register", "get": "get_user_count"})),
    path("user/", views.UserAPIView.as_view()),
]