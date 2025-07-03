from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import FileUpload, User
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
# Create your tests here.

class UserFlowTest(APITestCase):
    def setUp(self):
        self.ops_user = User.objects.create_user(
            username='opsuser@example.com',
            email="opsuser@example.com",
            password='password123',
            role='ops',
            is_email_verified=True)
        self.client_user = User.objects.create_user(
            username='clientuser@example.com',
            email="clientuser@example.com",
            password='password123',
            role='client',
            is_email_verified=True)
        self.ops_token = Token.objects.create(user=self.ops_user)
        self.client_token = Token.objects.create(user=self.client_user)
    
    def test_signup(self):
        url=reverse('signup')
        data= {
            'email': 'newclient@example.com',
            'password': 'password123',
            'role': 'client'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_login(self):
        url = reverse('api_token_auth')
        data = {
            'username': 'clientuser@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_file_upload(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.ops_token.key)
        url=reverse('file-upload')
        file=SimpleUploadedFile(
            name='testfile.pptx',
            content=b'This is a test file.',
            content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_file_upload_invalid_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token.key)
        url=reverse('file-upload')
        file=SimpleUploadedFile(
            name='testfile.txt',
            content=b'This is a test file.',
            content_type='text/plain'
        )
        response = self.client.post(url, {'file': file})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_generate_download_link(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.ops_token.key)
        file = SimpleUploadedFile("test.docx", b"content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        upload_response = self.client.post(reverse('file-upload'), {'file': file})
        file_id = FileUpload.objects.last().id

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.client_token.key)
        response = self.client.get(reverse('generate-download', args=[file_id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('download_link', response.data)