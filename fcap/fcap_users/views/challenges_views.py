
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


def challenge_requests(request):
    challenges_list = Challenge.objects.exclude(created_by = request.user.account)
    challenges = [] 
    player = []
    for challenge in challenges_list:
        try:
            ch = Challenge_Participant.objects.get(challenge = challenge, player = request.user.account)
        except:
            ch = None
        if ch:
            challenges.append(challenge)
            player.append(ch)
    
    
    context = {
        'challenges': challenges,
        'player': player
    }
    # print(challenges)
    return render(request, 'matches/challenge_requests.html', context)

def get_challenge(request, pk):
    challenge = Challenge.objects.get(id = pk)
    challengers = Challenge_Participant.objects.filter(challenge = challenge)

    context = {
        'challenge': challenge,
        'challengers': challengers
    }
    fh = False 
    for challenger in challengers: 
        if challenger.status == 'rejected':
            messages.error("Challenge has been Rejected by one or more of the Challengers. ")
            fh = True 
            break
    
    if not fh: 
        for challenger in challengers:
            if challenge.status != 'accepted':
                fh = False
    if not fh:
        messages.warning(request, "Awaiting the Response of Challengers. All Challengers must respond by " + str(challenge.expiry_time) + "\
            , otherwise the challenge will be removed. ")
    else:
        messages.success(request, "All Challengers have accepted the Challenge! \n"\
            "Please make the Payment of Rs. " + str(len(challengers) * 50) + " /= to the following account to Schedule your Challenge"\
                "\nName: Samman Nasir\nEasypaisa Jazzcash\nNumber: 03331234567\n"\
                "\nAfter the payment, send the screenshot to the given number.")

        
    return render(request, 'matches/challenge.html', context)