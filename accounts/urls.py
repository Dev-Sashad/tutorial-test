from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name= 'signup'),
    path('login', views.LoginView.as_view(), name= 'login'),
    path('getJwtToken', TokenObtainPairView.as_view(), name= 'getJwtToken'),
    path('refreshToken', TokenRefreshView.as_view(), name= 'refreshToken'),
    path('verifyToken', TokenVerifyView.as_view(), name= 'verifyToken')
]
