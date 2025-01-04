from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


User = get_user_model()

def create_jwt_pair_for_user(user:User):

    refresh = RefreshToken.for_user(user)
    token = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }
    return token