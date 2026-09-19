from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Notes(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title=models.CharField(max_length=300)
  description=models.TextField()
  image=models.ImageField(upload_to="notes/",blank=True,null=True)
  created_at =models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title


class EmailVerificationOTP(models.Model):
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE
  )
  otp = models.CharField(max_length=6)
  created_at = models.DateTimeField(auto_now_add=True)
  is_verified = models.BooleanField(default=False)

  def __str__(self):
    return self.user.email


class PasswordResetOTP(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  otp = models.CharField(max_length=6)
  created_at = models.DateTimeField(auto_now_add=True)
  is_verified = models.BooleanField(default=False)

  def is_expired(self):
    return timezone.now() > self.created_at + timezone.timedelta(minutes=5)