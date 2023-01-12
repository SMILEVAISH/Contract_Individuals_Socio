from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from userApp.models import CustomUser as user







class UserSerializer(serializers.ModelSerializer):
    country = CountryField()
    class Meta:
        model = user
        fields = ('email', 'mobile_number', 'first_name', 'last_name', 'gender', 'date_of_birth', 'user_category', 'country','password')
        extra_kwargs = {'password' : {'write_only':True}}

    def validate_email(self, value):
        if user.objects.filter(email = value).exists():
            raise serializers.ValidationError({
                'message' : 'Email_id already exists'
            })
        return value
    
    def validate(self, attrs):
        email_id = attrs.get('email', '')
        return attrs

    def create(self, validated_data):
        return user.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length = 128)
    # otp_generated = serializers.CharField(required = False)