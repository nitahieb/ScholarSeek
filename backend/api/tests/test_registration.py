from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.serializers import UserSerializer

class UserRegistrationTest(APITestCase):
    def test_registration_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "registration_code": "Register123"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_registration_invalid_code(self):
        data = {
            "username": "baduser",
            "email": "bad@example.com",
            "password": "password123",
            "registration_code": "WrongCode"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("registration_code", serializer.errors)

    def test_registration_missing_code(self):
        data = {
            "username": "nocodeuser",
            "email": "nocode@example.com",
            "password": "password123"
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("registration_code", serializer.errors)
