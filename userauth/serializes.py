from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","password","name","phone")
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        User.objects.filter(
            email = user
        ).update(
            name = validated_data['name'],
            phone = validated_data['phone']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    email = serializers.EmailField()
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
