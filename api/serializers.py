from rest_framework import serializers
from main.models import Notes
from django.contrib.auth.models import User


class NotesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notes
    fields ='__all__'


class RegisterSerializer(serializers.ModelSerializer):
  password =serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields=['username','password']

  def create(self,validated_data):
    user =User.objects.create_user(
      username=validated_data['username'],
      password=validated_data['password']
    )
    return user