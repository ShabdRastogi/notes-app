from rest_framework import serializers
from main.models import Notes
from django.contrib.auth.models import User
import re


class NotesSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notes
    fields = [
      "note_number",
      "title",
      "description",
      "image",
      "created_at",
      "updated_at",
    ]

    read_only_fields = [
      "note_number",
      "created_at",
      "updated_at",
    ]

class NotesPaginationSerializer(serializers.Serializer):
  count = serializers.IntegerField()
  next = serializers.URLField(allow_null=True)
  previous = serializers.URLField(allow_null=True)
  results = NotesSerializer(many=True)


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username','email','password']
	def validate_username(self, value):
		username_pattern = r'^[a-zA-Z0-9_-]{3,16}$'
		if not re.match(username_pattern, value):
			raise serializers.ValidationError(
				"Username must be 3 to 16 characters and use only letters, numbers, _ or -."
			)
		if User.objects.filter(username=value).exists():
			raise serializers.ValidationError(
				"Username already exists."
			)
		return value

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError(
				"An account with this email already exists."
			)
		return value

	def validate_password(self, value):
		password_pattern = (
			r'^(?=.*[A-Z])'
			r'(?=.*[a-z])'
			r'(?=.*[0-9])'
			r'(?=.*[@$!%*?&])'
			r'[A-Za-z0-9@$!%*?&]{8,}$'
		)
		if not re.match(password_pattern, value):
			raise serializers.ValidationError(
				"Password must be 8+ characters and contain "
				"one uppercase letter, one lowercase letter, "
				"one number, and one special symbol."
			)
		return value
	
	def create(self,validated_data):
		user = User.objects.create_user(
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

	def validate_otp(self, value):
		if not value.isdigit():
			raise serializers.ValidationError(
				"OTP must contain only numbers."
			)
		return value


class ResetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	new_password = serializers.CharField(
		write_only=True,
		min_length=8
	)
	def validate_new_password(self, value):
		password_pattern = (
			r'^(?=.*[A-Z])'
			r'(?=.*[a-z])'
			r'(?=.*[0-9])'
			r'(?=.*[@$!%*?&])'
			r'[A-Za-z0-9@$!%*?&]{8,}$'
		)
		if not re.match(password_pattern, value):
			raise serializers.ValidationError(
				"Password must be 8+ characters and contain "
				"one uppercase letter, one lowercase letter, "
				"one number, and one special symbol."
			)
		return value

