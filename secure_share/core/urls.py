from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import FileUploadView,GenerateDownloadLinkView, SecureDownloadView,SignupView,VerifyEmailView
urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'), 
    path('signup/', SignupView.as_view(), name='signup'),
    path('download-link/<int:file_id>/', GenerateDownloadLinkView.as_view(), name='generate-download'),
    path('download/<str:token>/', SecureDownloadView.as_view(), name='secure-download'),
    path('login/',obtain_auth_token,name='api_token_auth'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
]