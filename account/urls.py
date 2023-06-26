
from django.urls import path
from .views import Login, RegisterUserAPIView, ChangePasswordView, EmailAPI, Profile, DoFollow

app_name = 'account'
urlpatterns = [
  path("get-details/", Login),
  path('register/', RegisterUserAPIView.as_view()),
  path('change-password/', ChangePasswordView.as_view()),
  path('send-email/', EmailAPI.as_view()),
  path('profile/',Profile.as_view()),
  path('profile/<int:pk>/',Profile.as_view()),
  path('followers/',DoFollow.as_view()),
  path('follow/<int:pk>/',DoFollow.as_view()),


]

