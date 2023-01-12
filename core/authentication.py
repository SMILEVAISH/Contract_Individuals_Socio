from django.contrib.auth.backends import ModelBackend
from django_otp import models
from django.contrib.auth import get_user_model

class OTPBackend(ModelBackend, models.OTPBase):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None

        if not self.supports_otp(user):
            return None

        if not self.verify_token(user, password):
            return None

        return user
