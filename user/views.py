from django.shortcuts import render
import json
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, VerifyOtpSerializer, UserRegisterVerifySerializer, LoginSerializer, ShowinfoSerializer
from .two_factor import verify_otp
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login



class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.register()
        request.session['data'] = request.data
        return Response(json.loads(response.text), status=status.HTTP_201_CREATED)


class VerifyRegisterOtpView(APIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request, session_id, format=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        session = request.session['data']
        response = verify_otp(session_id, data['otp'])
        if response.status_code == 200:
            user_serializer = UserRegisterVerifySerializer(data=session)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            return Response({"message": "Register successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(json.loads(response.text), status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            user_serializer = ShowinfoSerializer(user)
            if user is not None:
                login(request, user)
                token = RefreshToken.for_user(user)
                data = {
                    'refresh': str(token),
                    "access": str(token.access_token),
                    'user_serializer': user_serializer.data
                }
                return Response(data)
            return Response({'message':'Invalid email or password!!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


