from django.urls import path
from .views import Feed

urlpatterns = [
    path('create-post/',Feed.as_view(),name='createPost'),
    path('create-post/<int:pk>/',Feed.as_view(),name='createPost'),

]