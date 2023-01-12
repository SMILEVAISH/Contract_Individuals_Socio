import random
from django.core.mail import send_mail
from core import settings

from celery import shared_task

def generate_otp():
    otp = random.randint(1000,9999)
    return otp

@shared_task(bind = True)
def otp_email(self, email,otp):
    # otp = random.randint(1000,9999)
    # print(otp)
    self.otp = otp 
    print('task started')
    send_mail(
            subject = "Your Login OTP",
            message= f'here is your 4 digit otp: {self.otp}',
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [email],
            fail_silently= False,
        )
    return f'Successfully sent otp: {otp}'
