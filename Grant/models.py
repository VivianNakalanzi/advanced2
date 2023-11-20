from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    fullname=models.CharField(max_length=100)
    email=models.EmailField()
    organizationName=models.CharField(max_length=250)
    organizationType=models.CharField(max_length=100)
