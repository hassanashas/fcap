from django.contrib import admin
from . models import Account, Challenge_Participant, Match, Participant, Challenge
# Register your models here.
admin.site.register(Account)
admin.site.register(Match)
admin.site.register(Participant)
admin.site.register(Challenge)
admin.site.register(Challenge_Participant)