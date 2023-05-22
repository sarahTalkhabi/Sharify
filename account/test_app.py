import os
from unittest import TestCase
import django
django.setup()
from django.contrib.auth import get_user
from django.urls import reverse
from django.conf import settings
from sys import path as sys_path
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User



class test_logInUser(APITestCase):

    def test_login(self):
        client = APIClient()
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username='admin', password='password12')
        self.assertTrue(get_user(self.client).is_authenticated)



