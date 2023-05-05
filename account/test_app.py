import os
from unittest import TestCase
import django
django.setup()
from django.urls import reverse
from django.conf import settings
from sys import path as sys_path
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User



class test_Account(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """

        self.assertEqual(2, 1)
    def test_login(self):
        client = APIClient()
        client.login(username='admin', password='password12')

