from .models import User
from rest_framework import serializers
from .two_factor import send_authentication_otp
from django.contrib.auth.hashers import make_password

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'phone', 'date_of_birth', 'password']

    def validate_phone(self, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise serializers.ValidationError("Please enter valid phone number")
        return phone

    def register(self, **kwargs):
        phone = self.validated_data.pop('phone')
        users = User.objects.filter(phone=phone)
        if not users:
            response = send_authentication_otp(phone)
            return response
        else:
            raise serializers.ValidationError(
                {"message": ["Your mobile number is already registered"]})


class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()

class UserRegisterVerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'phone', 'date_of_birth', 'password']

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        password = make_password(pwd)
        user = User.objects.create(password=password, **validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(max_length=254)

    class Meta:
        model = User
        fields = ['email', 'password']


class ShowinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']
                  

