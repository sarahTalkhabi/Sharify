import json
import os
from unittest import TestCase
import django

django.setup()
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User


class test_logInUser(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='UsertestPass!#', email='usertset@example.com')
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    def test_user_register(self):
        data = {
            "username": 'testRegisteruser',
            "password": 'UsertestPass!#',
            "email": 'testRegisteruser@example.com',

        }
        post = self.client.post('/register/', data, format='json')
        self.assertEquals(post.status_code, status.HTTP_201_CREATED)

    def test_user_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION='token' + self.token.key)
        response = self.client.get('/get-details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        new_data = {
            "old_password": "UsertestPass!#",
            "new_password": "NewUsertestPass!#"
        }
        self.client.credentials(HTTP_AUTHORIZATION='token' + self.token.key)
        request = self.client.put('/change-password/', new_data)



    def test_create_profile(self):
        data = {

                "id": 1,
                "user": 5,
                "firstName": 'testProfile',
                "lastName": 'TestProfile',
                "location": "paris",
                "bio": "this is bio",
                "image": 'null',
                "followers": []
        }
        self.client.credentials(HTTP_AUTHORIZATION='token' + self.token.key)
        request = self.client.put('/profile/', data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)