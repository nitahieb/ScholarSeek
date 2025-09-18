
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import RegistrationCode


class RegistrationCodeModelTests(TestCase):
    def test_create_code(self):
        """Test creating a registration code"""
        code = RegistrationCode.create_code("TEST123", 30)
        self.assertEqual(code.code, "TEST123")
        self.assertFalse(code.is_used)
        self.assertTrue(code.is_valid())

    def test_expired_code(self):
        """Test that expired codes are invalid"""
        code = RegistrationCode.create_code("EXPIRED", -1)  # Expired yesterday
        self.assertFalse(code.is_valid())

    def test_use_code(self):
        """Test using a registration code"""
        code = RegistrationCode.create_code("USETEST", 30)
        user = User.objects.create_user(username='testuser', email='test@example.com')

        code.use_code(user)

        self.assertTrue(code.is_used)
        self.assertEqual(code.used_by, user)
        self.assertIsNotNone(code.used_at)
        self.assertFalse(code.is_valid())


class RegistrationAPITests(APITestCase):
    def setUp(self):
        self.valid_code = RegistrationCode.create_code("VALID123", 30)
        self.expired_code = RegistrationCode.create_code("EXPIRED", -1)
        self.register_url = reverse('register')

    def test_register_with_valid_code(self):
        """Test successful registration with valid code"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123',
            'registration_code': 'VALID123'
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Code should be marked as used
        self.valid_code.refresh_from_db()
        self.assertTrue(self.valid_code.is_used)

    def test_register_with_invalid_code(self):
        """Test registration fails with invalid code"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123',
            'registration_code': 'INVALID'
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('registration_code', response.data)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_with_expired_code(self):
        """Test registration fails with expired code"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123',
            'registration_code': 'EXPIRED'
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('registration_code', response.data)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_without_code(self):
        """Test registration fails without code"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('registration_code', response.data)
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_with_used_code(self):
        """Test registration fails with already used code"""
        # First user uses the code
        first_user = User.objects.create_user(username='first', email='first@example.com')
        self.valid_code.use_code(first_user)

        # Second user tries to use the same code
        data = {
            'username': 'second',
            'email': 'second@example.com',
            'password': 'testpass123',
            'registration_code': 'VALID123'
        }
        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('registration_code', response.data)
        self.assertFalse(User.objects.filter(username='second').exists())
