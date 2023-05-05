
from django.urls import path
from .views import profileAPI,RegisterUserAPIView, ChangePasswordView
urlpatterns = [
  path("get-details/",profileAPI),
  path('register/',RegisterUserAPIView.as_view()),
  path('change-password/',ChangePasswordView.as_view()),
]

