from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class Account(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=False, default="blank")
    profile_pic = models.ImageField(null=True, blank=True)
    ratings = models.FloatField(default=1000)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    phone = models.CharField(max_length=255, null=True)

class Match(models.Model):

    player1 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = 'player2')
    match_time = models.DateTimeField(null=True)
    player1_points = models.FloatField(null=True)
    player2_points = models.FloatField(null=True)