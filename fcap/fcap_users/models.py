from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    ratings = models.FloatField(default=1000)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
