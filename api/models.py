from django.db import models

# Create your models here.

class Api(models.Model):
  user = models.CharField(max_length = 200)
  age = models.IntegerField()

  def __str__(self):
    return self.name
