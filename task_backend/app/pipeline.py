from django.contrib.auth import get_user_model
from .tasks import generate_verification_code, send_verification_code_email
User = get_user_model()

def send_welcome_email_celery(strategy, details, **kwargs):
    email = details.get('email')
    print(email)
    verification_code = generate_verification_code()
    try:
        user = User.objects.get(email=email)
        send_verification_code_email.delay(email, verification_code)
    except User.DoesNotExist:
        user = User.objects.create_user(email=email)
        send_verification_code_email.delay(email, verification_code)
