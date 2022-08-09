
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .views import findDuplicate
from ..models import Account, Participant, Match, Challenge, Challenge_Participant
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

def challenges(request):
    challenges = Challenge.objects.filter(created_by = request.user.account)
    context = {
        'challenges': challenges
    }
    return render(request, 'matches/challenges.html', context)


@login_required(login_url = 'login')
def add_new_challenge(request):

    context = {

    }
    if request.method == "POST":
        print(request.POST)
        totalPlayers = int(request.POST['players']) + 1
        # Error Checking 
        players_list = [] 
        for index in range(1, totalPlayers):
            username = request.POST['player_select' + str(index)]
            
            if username == "None":
                messages.error(request, "Player Name can't be empty")
                return render(request, 'matches/add_new_challenge.html', context)
            
            challenger_account = Account.objects.get(user = User.objects.get(username=username))
            players_list.append(challenger_account)

        if findDuplicate([i for i in players_list]):
            messages.error(request, "All Players must be Unique in the Challenge")
            return render(request, 'matches/add_new_challenge.html', context)

        challenge = Challenge.objects.create(totalPlayers=totalPlayers-1, 
                                            match_time=make_aware(datetime.strptime(request.POST['date'], '%Y-%m-%dT%H:%M')), 
                                            expiry_time=make_aware(datetime.strptime(request.POST['expiry_date'], '%Y-%m-%dT%H:%M')),
                                    created_by = request.user.account)

        for player in players_list:
            Challenge_Participant.objects.create(challenge = challenge, player = player)
        Challenge_Participant.objects.create(challenge = challenge, player = request.user.account, status = "accepted")
        messages.success(request, "New Challenge has been Created! Awaiting Challenger(s)' Acceptance")
        return redirect('challenges')

    return render(request, 'matches/add_new_challenge.html')


# class GetPlayerChallenges(APIView):
#     def get(self, request, format=None):
#         challenges = Challenge.objects.filter(created_by = request.user.account).values()
#         challenges_list = []
#         for challenge in challenges: 
#             challenges_list.append(challenge)
        
#         data = {
#             'challenges': challenges_list
#         }

#         return Response(data)