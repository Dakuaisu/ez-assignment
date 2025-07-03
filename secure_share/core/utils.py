from itsdangerous import URLSafeTimedSerializer

def get_token_serializer():
    from django.conf import settings
    return URLSafeTimedSerializer(settings.SECRET_KEY, salt='secure-download')
