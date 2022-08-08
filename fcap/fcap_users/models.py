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

    match_time = models.DateTimeField(null=True)
    totalPlayers = models.IntegerField(default=2)
    winner = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-match_time']

class Participant(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Account, on_delete=models.CASCADE)
    player_points = models.FloatField(null=True)
    player_prev_ratings = models.FloatField(null=True)
    player_new_ratings = models.FloatField(null=True)

class Challenge(models.Model):
    match_time = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, default="pending")

class Challenge_Participant(models.Model):
    player = models.ForeignKey(Account, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)