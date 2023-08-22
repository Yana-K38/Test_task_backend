from celery import shared_task
from django.core.mail import send_mail
import random
from django.core.cache import cache

def generate_and_store_verification_code(email):
    verification_code = generate_verification_code()
    cache_key = f'verification_code_{email}'
    cache.set(cache_key, verification_code, timeout=300)

def is_valid_verification_code(email, entered_code):
    cache_key = f'verification_code_{email}'
    stored_code = cache.get(cache_key)

    if stored_code and stored_code == entered_code:
        cache.delete(cache_key)
        return True
    else:
        return False

def generate_verification_code():
    code_length = 6
    verification_code = ''.join(random.choice('0123456789') for _ in range(code_length))
    return verification_code

@shared_task
def send_verification_code_email(email, verification_code):
    subject = 'Verification Code'
    message = f'Your verification code is: {verification_code}'
    from_email = 'kurzukova.yana@yandex.ru'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)