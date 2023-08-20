from datetime import timedelta
from django.utils import timezone
import random
import string
from django.core.mail import send_mail

class OTPManager:
    otp_store = {}

    @staticmethod
    def generate_otp(length=6):
        return ''.join(random.choices(string.digits, k=length))

    @classmethod
    def generate_and_store_otp(cls, email):
        otp = cls.generate_otp()
        cls.otp_store[email] = {
            'otp': otp,
            'expires_at': timezone.now() + timedelta(seconds=60)
        }
        return otp

    @classmethod
    def validate_otp(cls, email, otp):
        stored_otp_data = cls.otp_store.get(email)
        if stored_otp_data and stored_otp_data['otp'] == otp and stored_otp_data['expires_at'] > timezone.now():
            del cls.otp_store[email]
            return True
        return False


def send_otp_email(email):
    otp = OTPManager.generate_and_store_otp(email)
    
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = 'kurzukova.yana@yandex.ru'
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)