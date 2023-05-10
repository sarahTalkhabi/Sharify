from datetime import datetime

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Post


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        post = Post.objects.create(
            creator=CurrentUserDefault,
            text=validated_data['text'],
            image=validated_data['image'],
            video=validated_data['video'],
            date=datetime.now()
        )

        post.save()
        return post
