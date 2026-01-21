import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def generate_verification_token():
    """Generate a secure random token for email verification"""
    return secrets.token_urlsafe(32)


def send_verification_email(user):
    """Send email verification link to user"""
    token = generate_verification_token()
    user.email_verification_token = token
    user.save()
    
    verification_url = f"{settings.BACKEND_URL}/api/auth/verify-email/?token={token}"
    api_endpoint = f"{settings.BACKEND_URL}/api/auth/verify-email/"
    
    subject = 'Verify Your Email Address'
    message = f"""
    Hello {user.get_full_name() or user.username},
    
    Thank you for registering! Please verify your email address.
    
    Option 1: Click the verification link below:
    {verification_url}
    
    Option 2: Make a POST request to the API endpoint:
    POST {api_endpoint}
    Body: {{"token": "{token}"}}
    
    If you did not create an account, please ignore this email.
    
    Best regards,
    Your App Team
    """
    
    html_message = f"""
    <html>
    <body>
        <h2>Verify Your Email Address</h2>
        <p>Hello {user.get_full_name() or user.username},</p>
        <p>Thank you for registering! Please verify your email address.</p>
        <p><strong>Option 1:</strong> Click the link below:</p>
        <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
        <p><strong>Option 2:</strong> Make a POST API call:</p>
        <p><strong>Endpoint:</strong> {api_endpoint}</p>
        <p><strong>Method:</strong> POST</p>
        <p><strong>Body:</strong></p>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px;">{{"token": "{token}"}}</pre>
        <p>Or copy and paste this link into your browser:</p>
        <p>{verification_url}</p>
        <p>If you did not create an account, please ignore this email.</p>
        <p>Best regards,<br>Your App Team</p>
    </body>
    </html>
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
