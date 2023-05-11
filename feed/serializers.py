from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Post
        fields = '__all__'
