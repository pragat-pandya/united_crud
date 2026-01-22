from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password,])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializer.ValidationError({"password": "Password is not matching with password2"})
        return attrs
    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validate_password)
        return user
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'password2'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'date_of_birth', 
            'date_joined', 
            'email_verified'
        )
    

class CustomTokenObtainPairSerilaizer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        user = self.user

        if not user or user.email_verified == False:
            # if not user or not user.email_verified:
            raise AuthenticationFailed(
                "Auth Failed!"
            )
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['email_verified'] = user.email_verified
        return token