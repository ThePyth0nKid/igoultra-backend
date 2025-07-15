from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class MeEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('custom_me_view')  # /api/v1/auth/me/

    def test_delete_own_account(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.filter(username='testuser').count(), 0)
        # Bei 204 No Content gibt es keine response.json(), daher keine weitere Prüfung

    def test_is_staff_in_user_serializer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertIn('is_staff', data)
        self.assertTrue(data['is_staff'])

class UserSerializerTests(TestCase):
    def test_is_staff_field_output(self):
        user = User(username='staffuser', is_staff=True)
        serializer = UserSerializer(user)
        self.assertIn('is_staff', serializer.data)
        self.assertTrue(serializer.data['is_staff'])

    def test_is_staff_field_output_false(self):
        user = User(username='normaluser', is_staff=False)
        serializer = UserSerializer(user)
        self.assertIn('is_staff', serializer.data)
        self.assertFalse(serializer.data['is_staff'])
