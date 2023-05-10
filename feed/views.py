from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Post
from rest_framework.response import Response

from .serializers import CreatePostSerializer


# Create your views here.

class Feed(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = self.request.user
        posts = Post.objects.filter(creator=user)
        return Response(posts)

    def post(self, request):
        serializer = CreatePostSerializer(data=request.data)

