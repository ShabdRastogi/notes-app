from rest_framework import serializers
from main.models import Notes
from django.contrib.auth.models import User


class NotesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notes
    fields ='__all__'
    read_only_fields = ['user']


class RegisterSerializer(serializers.ModelSerializer):
  password =serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields=['username','email','password']

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError(
        "An account with this email already exists."
      )
    return value

  def create(self,validated_data):
    user =User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password']
    )
    return user

class VerifyOTPSerializer(serializers.Serializer):
  email = serializers.EmailField()
  otp = serializers.CharField(
    max_length=6,
    min_length=6
  )

class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )