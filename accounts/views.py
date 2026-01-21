from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer
from .utils import send_verification_email


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        # Check if email is verified
        if not user.email_verified:
            raise AuthenticationFailed(
                'Please verify your email address before logging in. Check your email for the verification link.'
            )
        
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['email_verified'] = user.email_verified
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification email
        email_sent = send_verification_email(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'User registered successfully. Please check your email to verify your account.',
            'email_sent': email_sent
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def _verify_email(self, token):
        """Helper method to verify email with token"""
        if not token:
            return Response(
                {'error': 'Verification token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email_verification_token=token)
            
            if user.email_verified:
                return Response(
                    {'message': 'Email is already verified.'},
                    status=status.HTTP_200_OK
                )
            
            user.email_verified = True
            user.email_verification_token = None
            user.save()
            
            return Response(
                {'message': 'Email verified successfully. You can now log in.'},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired verification token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request, *args, **kwargs):
        """Handle GET request for direct link clicks"""
        token = request.query_params.get('token')
        return self._verify_email(token)
    
    def post(self, request, *args, **kwargs):
        """Handle POST request for API calls"""
        token = request.data.get('token')
        return self._verify_email(token)
