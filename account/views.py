from django.shortcuts import render
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile, UserFollowing
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, SendEmailSerializer, \
    profileSerializer, followerSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.authtoken.models import Token


@api_view(['GET'])
# Class based view to Get User Details using Token Authentication
def Login(request):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    data = request.data
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


def not_duplicate(id):
    try:
        if UserProfile.objects.get(user=id) is None:
            return False
    except ObjectDoesNotExist:
        return True


def get_profile(id):
    try:
        return UserProfile.objects.get(user=id)
    except ObjectDoesNotExist:
        return None


class Profile(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = get_profile(request.user.id)
        serializer = profileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = profileSerializer(data=request.data)
        if serializer.is_valid():
            if not_duplicate(request.user.id):
                serializer.save(user=request.user)
            else:
                return Response(status=status.HTTP_302_FOUND)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        profile = get_profile(pk)
        if profile is None:
            return Response({'error': 'profile not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = profileSerializer(profile, request.data, partial=True)
        if serializer.is_valid():
            if profile.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Yoo are not authorized to change the profile'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class DoFollow(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        profile = get_profile(request.user.id)
        serializer = followerSerializer(profile)
        return Response(serializer.data)

    def post(self, request, pk):
        UserFollowing.objects.create(user_id=request.user,
                                     following_user_id=get_profile(pk))
        profile = get_profile(request.user.id)
        serializer = followerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)

    def delete(self):
        pass


class EmailAPI(APIView):
    def get(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.data.get('subject')
            txt_ = serializer.data.get('text')
            html_ = serializer.data.get('html')
            recipient_list = serializer.data.get('recipient_list')
            from_email = settings.DEFAULT_FROM_EMAIL
            if subject is None and txt_ is None and html_ is None and recipient_list is None:
                return Response({'msg': 'There must be a subject, a recipient list, and either HTML or Text.'},
                                status=200)
            elif html_ is not None and txt_ is not None:
                return Response({'msg': 'You can either use HTML or Text.'}, status=200)
            elif html_ is None and txt_ is None:
                return Response({'msg': 'Either HTML or Text is required.'}, status=200)
            elif recipient_list is None:
                return Response({'msg': 'Recipient List required.'}, status=200)
            elif subject is None:
                return Response({'msg': 'Subject required.'}, status=200)
            else:
                sent_email = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list.split(','),
                    html_message=html_,
                    fail_silently=False,
                )
                return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
