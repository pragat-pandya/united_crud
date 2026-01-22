from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, UserSerializer
from .models import User
from .utils import send_verification_email
# Create your views here.


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        email_sent = send_verification_email()
        return Response({
            'user' : UserSerializer(user).data,
            'message': 'User Registered Successfully. Please check email to verify account.',
            'email_sent' : email_sent
        }, status=status.HTTP_201_CREATED)





# LOGIN API
# class CustomTokenObtainView(TokenObtainPairView):
