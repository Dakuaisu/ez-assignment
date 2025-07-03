# Secure File Sharing System – Backend Assignment

## 🔧 Tech Stack
- Django + Django Rest Framework
- SQLite (can be replaced with PostgreSQL)
- Token Authentication
- itsdangerous for secure download URLs

## 👥 Users
- **Ops User**: Upload `.pptx`, `.docx`, `.xlsx` files
- **Client User**: Sign up, verify email, list/download securely

## 📦 Features
- Token-based login
- Email verification with 1-hour expiry
- File validation and secure file upload
- Encrypted one-time download links
- REST APIs fully tested with DRF's `APITestCase`

## 🧪 How to Test
1. Run the server:
   ```bash
   python manage.py runserver
