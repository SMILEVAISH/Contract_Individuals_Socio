from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django_countries.fields import CountryField

from django.contrib.auth.hashers import make_password


from userApp.managers import CustomUserManager

mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',message ='Phone number is not valid')

genderChoices = (
    ('male','male'),('female','female')
)

category_choices = (
    ('individual','individual'),
    ('contractor', 'contractor')
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(blank=True,max_length=14, validators= [mobile_regex])
    first_name = models.CharField(max_length=100, blank = True)
    last_name = models.CharField(max_length = 100, blank = True)
    gender = models.CharField(choices= genderChoices, max_length=10)
    date_of_birth = models.DateField(blank=True, null=True)
    user_category = models.CharField(choices = category_choices, max_length=20, default='individual')
    country = CountryField(blank_label = '(select country)', blank=True)
    password = models.CharField(max_length=266, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ email, mobile_number, first_name, last_name, gender, date_of_birth, user_category, country, password]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        # return super().set_password(raw_password)
    
