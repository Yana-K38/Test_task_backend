from app.tasks import send_otp_email

def send_otp_code(backend, user, response, *args, **kwargs):
    send_otp_email(user, *args, **kwargs)