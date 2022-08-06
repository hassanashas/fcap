from django.shortcuts import render, redirect
from django.views import View
import json 
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.models import User
from .forms import AccountForm, UserForm
from django.contrib.auth import authenticate, login, logout
from .models import Account, Participant, Match
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import json 
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from django.db.models import Avg, Count, Min, Sum
import numpy as np 
from multielo import MultiElo

from collections import Counter # For Duplicate Finding 
rank_system = MultiElo()

# Create your views here.

@login_required(login_url='login')
def index(request): 
    matches = Match.objects.all()
    context = {
        'matches': matches
    }
    return render(request, 'user/dashboard.html', context)

@login_required(login_url = 'login')
def add_match(request):
    accounts = Account.objects.all()
    accounts_list = []
    for account in accounts:
        accounts_list.append((account.name, account.user.username))
    accounts = json.dumps(accounts_list)
    context = {
        "accounts": accounts
    }

    if request.method == "POST": 
        totalPlayers = int(request.POST['players']) + 1
        # Error Checking 
        players_list = [] 
        for index in range(1, totalPlayers):
            username = request.POST['player_select' + str(index)]
            player_score = request.POST['player_score' + str(index)]
            
            if username == "None":
                messages.error(request, "Player Name can't be empty")
                return render(request, 'matches/add_match.html', context)
            if not player_score:
                messages.error(request, "Player Points can't be empty")
                return render(request, 'matches/add_match.html', context)
            player_score = int(player_score)
            if player_score < 0 or player_score > 120:
                messages.error(request, "Player Points must be between 0 and 120")
                return render(request, 'matches/add_match.html', context)
            part_account = Account.objects.filter(user = User.objects.filter(username=username)[0])[0]
            players_list.append((part_account, player_score))

        if findDuplicate([i[0] for i in players_list]):
            messages.error(request, "All Players must be Unique in the Match")
            return render(request, 'matches/add_match.html', context)

        # Match Creation
        match = Match.objects.create(totalPlayers=totalPlayers-1, match_time=make_aware(datetime.strptime(request.POST['date'], '%Y-%m-%dT%H:%M')))
        
        
        for index in range(1, totalPlayers):
            username = request.POST['player_select' + str(index)]
            player_score = int(request.POST['player_score' + str(index)])
            part_account = Account.objects.filter(user = User.objects.filter(username=username)[0])[0]
            Participant.objects.create(match=match, player = part_account, player_points = player_score)

        
        # Getting the Winner of the Game
        players_list.sort(key = lambda x: x[1], reverse=True)
        winner = players_list[0][0]
        match.winner = winner
        match.save()
        
        # Getting new Ratings for Players 
        temp_list = []
        for player in players_list:
            temp_list.append(player[0].ratings)
        points_array = np.array(temp_list)
        new_rank = rank_system.get_new_ratings(points_array)
        for index in range(0, len(new_rank)):
            players_list[index][0].ratings = round(new_rank[index], 2)
            players_list[index][0].save()
        messages.success(request, "Match has been successfully added")
        return redirect('index')

    return render(request, 'matches/add_match.html', context)



def rankings(request):
    players = Account.objects.all() 
    players = Account.objects.annotate(matches=Count('participant')).order_by('-ratings')
    context = {
        'players': players
    }
    return render(request, 'matches/rankings.html', context)


def loginPage(request): 
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print(username, password, user)

        if user is not None: 
            login(request, user)
            return redirect('index')
    return render(request, 'user/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

def register(request): 
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        user = User.objects.create(username=request.POST['username'], email=request.POST['email'], password=make_password(request.POST['password1']))
        Account.objects.create(name=request.POST['name'], profile_pic = request.FILES['profile_pic'], user=user, phone=request.POST['phone'], password=request.POST['password1'])


    context = {}
    return render(request, 'user/register.html', context)

class EmailVerification(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({"email_error": "Entered Email is not Valid"}, status=400)
        if len(email) == 0:
            return JsonResponse({"email_error": "Email Field can not be Empty"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error": "Entered Email already exists"}, status=400)
        
        return JsonResponse({"email_valid": True})
        
class UsernameVerification(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if len(username) == 0:
            return JsonResponse({"username_error": "Username Field can not be Empty"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error": "Entered Username already exists"}, status=400)
        
        return JsonResponse({"username_valid": True})
        
class NameVerification(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data['name']

        if len(name) == 0:
            return JsonResponse({"name_error": "Name Field can not be Empty"}, status=400)
        if not name.replace(" ", "").isalpha():
            return JsonResponse({"name_error": "Entered Name is not Correct"}, status=400)
        
        return JsonResponse({"name_valid": True})
        

def findDuplicate(players_list):
    for k, v in Counter(players_list).items():
        if v > 1:
            return True
    return False 
