from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status

@api_view(['GET'])
# Class based view to Get User Details using Token Authentication
def profileAPI(request):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({"old_password": "Old password is not correct"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    permission_classes = (AllowAny,)

