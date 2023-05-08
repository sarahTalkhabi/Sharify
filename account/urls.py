
from django.urls import path
from .views import profileAPI, RegisterUserAPIView, ChangePasswordView, EmailAPI

urlpatterns = [
  path("get-details/",profileAPI),
  path('register/',RegisterUserAPIView.as_view()),
  path('change-password/',ChangePasswordView.as_view()),
  path('send-email/', EmailAPI.as_view()),
]

