from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.core.mail import send_mail
from itsdangerous import URLSafeTimedSerializer,BadSignature,SignatureExpired
from .models import User,FileUpload
from django.http import FileResponse
from .serializers import FileUploadSerializer
from .utils import get_token_serializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

SECRET_KEY= settings.SECRET_KEY

serializer =URLSafeTimedSerializer(SECRET_KEY)

class SignupView(APIView):
    def post(self,request):
        email=request.data['email']
        password=request.data['password']
        role=request.data['role']

        user=User.objects.create_user(username=email,email=email,password=password,role=role)
        token=serializer.dumps(email,salt='email-confirm')
        verify_url= f"http://localhost:8000/api/verify-email/{token}"
        send_mail(
            subject='Email Verification',
            message=f'Please click the link to verify your email: {verify_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        
        return Response({'message':"Signup successful.Please check your email."},status.HTTP_201_CREATED)



class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        if request.user.role != 'ops':
            return Response({'error': 'Only Ops Users can upload files.'}, status.HTTP_403_FORBIDDEN)
        serializer=FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_by=request.user)
            return Response({'message':'File Uploaded sucessfully.'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class GenerateDownloadLinkView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,file_id):
        if request.user.role!= 'client':
            return Response({'error': 'Only Client Users can request download links.'}, status.HTTP_403_FORBIDDEN)
        
        try:
            file=FileUpload.objects.get(id=file_id)
        except FileUpload.DoesNotExist:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=get_token_serializer()

        token=serializer.dumps({'file_id':file.id,'user_id':request.user.id})

        download_url=f"http://localhost:8000/api/download/{token}/"
        return Response({'download_link': download_url}, status=status.HTTP_200_OK)
    
class SecureDownloadView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,token):
        serializer=get_token_serializer()
        try:
            data=serializer.loads(token,max_age=3600)
            file_id=data['file_id']
            user_id =data['user_id']

            if request.user.id !=user_id:
                return Response({'error':'You are not authorized too access this file.'},status.HTTP_403_FORBIDDEN)
            file=FileUpload.objects.get(id=file_id)
            return FileResponse(file.file.open('rb'),as_attachment=True)
        except SignatureExpired:
            return Response({'error':'Download Link expired.'},status.HTTP_400_BAD_REQUEST)
        except (BadSignature,FileUpload.DoesNotExist):
            return Response({'error':'Invalid download link.'},status.HTTP_400_BAD_REQUEST)
    
class VerifyEmailView(APIView):
    def get(self, request, token):
        serializer = get_token_serializer()
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        except SignatureExpired:
            return Response({'error': 'Verification link expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except BadSignature:
            return Response({'error': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)