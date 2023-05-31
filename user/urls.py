from django.contrib import admin
from django.urls import path
from .views import RegisterView, VerifyRegisterOtpView, LoginView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='rest_register'),
    path('registration-verification/<str:session_id>',
         VerifyRegisterOtpView.as_view(), name='registration-verification'),
    path('login/', LoginView.as_view(), name='login'),
]