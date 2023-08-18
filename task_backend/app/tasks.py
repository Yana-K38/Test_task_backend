from celery import shared_task
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
from .models import OTP
import logging


def send_otp_email(user, *args, **kwargs):
    logging.debug(f"send_otp_email: user={user}")
    otp_code = get_random_string(length=6, allowed_chars='0123456789')
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = 'kurzukova.yana@yandex.ru'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

    OTP.objects.create(email=user.email, code=otp_code, expires_at=timezone.now() + timedelta(minutes=5))