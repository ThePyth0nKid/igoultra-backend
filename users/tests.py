from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from unittest.mock import patch, MagicMock
from django.test import override_settings

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

class AvatarS3EndpointsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='avataruser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.presign_url = reverse('avatar_presign')
        self.avatar_url = reverse('avatar')
        self.override = override_settings(
            AWS_ACCESS_KEY_ID='dummy',
            AWS_SECRET_ACCESS_KEY='dummy',
            AWS_STORAGE_BUCKET_NAME='bucket',
            AWS_REGION_NAME='region',
        )
        self.override.enable()

    def tearDown(self):
        self.override.disable()

    @patch('users.views.boto3')
    def test_avatar_presign(self, mock_boto3):
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        mock_client.generate_presigned_post.return_value = {'url': 'https://fake', 'fields': {}}
        data = {'file_name': 'test.png', 'file_type': 'image/png'}
        response = self.client.post(self.presign_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('url', response.data)
        self.assertIn('key', response.data)

    def test_avatar_patch_and_get(self):
        # Set avatar_url
        url = 'https://bucket.s3.region.amazonaws.com/avatars/1_test.png'
        response = self.client.patch(self.avatar_url, {'avatar_url': url}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.avatar_url, url)
        # Get avatar_url
        response = self.client.get(self.avatar_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['avatar_url'], url)

    @patch('users.views.boto3')
    def test_avatar_delete(self, mock_boto3):
        # Set avatar_url first
        url = 'https://bucket.s3.region.amazonaws.com/avatars/1_test.png'
        self.user.avatar_url = url
        self.user.save()
        mock_client = MagicMock()
        mock_boto3.client.return_value = mock_client
        response = self.client.delete(self.avatar_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.avatar_url)
        mock_client.delete_object.assert_called_once()
