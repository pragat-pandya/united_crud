import secrets
from django.conf import settings
from django.core.mail import send_mail

def generate_verification_token():
    return secrets.token_urlsafe(32)

def send_verification_email(user):
    token = generate_verification_token()
    user.email_verification_token = token
    user.save()

    verification_url = f"{settings.BACKEND_URL}/api/auth/verify-email/?token={token}"

    subject = "Verify Your Email"
    message = f"""
    Hello {user.get_full_name() or user.username},
    
    Thank you for registering! Please verify your email address.
    
    Option 1: Click the verification link below:
    {verification_url}
    
    If you did not create an account, please ignore this email.
    
    Best regards,
    Your App Team
    """

    html_message = f"""
    <html>
    <body>
        <h2>Verify Your Email Address</h2>
        <p>Hello {user.first_name},</p>
        <p>Thank you for registering! Please verify your email address.</p>
        <p><strong>Option 1:</strong> Click the link below:</p>
        <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
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
            recipint_list=[user.email],
            html_message=html_message,
            fail_silently=False
        )
        return True
    except Exception as e:
        print("Error sending the email")
        return False

