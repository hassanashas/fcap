from django.shortcuts import render, redirect
from django.views import View
import json 
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.models import User
from ..forms import AccountForm, UserForm
from django.contrib.auth import authenticate, login, logout
from ..models import Account, Participant, Match, Challenge
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import json 
from django.contrib import messages
from django.utils.timezone import make_aware
from datetime import datetime
from django.db.models import Avg, Count, Min, Sum, F
from django.db.models.expressions import Window
from django.db.models.functions import Rank
import numpy as np 
from multielo import MultiElo
from rest_framework.views import APIView
from rest_framework.response import Response
from collections import Counter # For Duplicate Finding 

# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    player = Account.objects.get(user = request.user)
    player_rank = Account.objects.filter(ratings__gte=player.ratings).count()
    matches_won = Match.objects.filter(winner = player).count()
    matches_played = Participant.objects.filter(player = player).count()
    # print(player.rank, player.name, player.user.username)
    context = {
        'player': player, 
        'player_rank': player_rank, 
        'matches_won': matches_won, 
        'matches_played': matches_played
    }

    return render(request, 'user/user_dashboard.html', context)


@login_required(login_url='login')
def index(request): 
    matches = Match.objects.all()
    context = {
        'matches': matches
    }
    return render(request, 'user/dashboard.html', context)

@login_required(login_url = 'login')
def add_match(request):
    accounts = Account.objects.all().order_by('user__username')
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
        
        players_list = [] 
        for index in range(1, totalPlayers):
            username = request.POST['player_select' + str(index)]
            player_score = int(request.POST['player_score' + str(index)])
            part_account = Account.objects.filter(user = User.objects.filter(username=username)[0])[0]
            participant = Participant.objects.create(match=match, player = part_account, player_points = player_score, 
                                                        player_prev_ratings=part_account.ratings)
            players_list.append((part_account, player_score, participant))

        
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
        # Creating a MultiElo Instance 
        n = len(points_array)
        # out = np.sum(points_array * np.arange(n-1, -n, -2) ) / (n*(n-1) / 2)
        rank_system = MultiElo(k_value = 32)
        new_rank = rank_system.get_new_ratings(points_array)
        for index in range(0, len(new_rank)):
            players_list[index][0].ratings = round(new_rank[index], 2)
            players_list[index][0].save()
            # Saving the Participant's new ratings. 
            players_list[index][2].player_new_ratings = round(new_rank[index], 2)
            players_list[index][2].save()
        messages.success(request, "Match has been successfully added")
        return redirect('index')

    return render(request, 'matches/add_match.html', context)



def rankings(request):
    players = Account.objects.all() 
    players = Account.objects.annotate(matches=Count('participant', distinct=True), total_points=Sum('participant__player_points'),
    matches_won = Count('match', distinct=True)).order_by('-ratings')
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


        if user is not None: 
            login(request, user)
            return redirect('dashboard')
        else: 
            messages.error(request, "Invalid Roll No or Password")
            return render(request, 'user/login.html')
    return render(request, 'user/login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect('login')

def register(request): 
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        
        username = request.POST['username']
        password = make_password(request.POST['password1'])
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        user = User.objects.create(username=username, email=email, password=password)
        account = Account.objects.create() 
        account.name = name 
        if request.FILES.get('profile_pic', None):
            profile_pic = request.FILES['profile_pic']
            account.profile_pic = profile_pic
        account.user = user
        account.phone = phone
        # account.profile_pic = profile_pic
        # account.save()  
        account.password = request.POST['password1']
        account.save()
        #Account.objects.create(name=name, profile_pic = profile_pic, user=user, phone=phone, password=request.POST['password1'])

        messages.success(request, "Account has been successfully created. Login to Continue")
        return redirect('login')


    context = {}
    return render(request, 'user/register.html', context)

@login_required(login_url='login')
def all_members(request):
    
    if request.method == 'POST':
        account = Account.objects.get(user__username = request.POST['username'])
        if account.type == 'Member':
            account.type = 'Admin'
        else:
            account.type = 'Member'
        account.save()
    accounts = Account.objects.order_by('type', 'user')
    context = {
        'accounts': accounts
    }

    
    return render(request, 'user/all_members.html', context)

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


def getData(request):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data)



def match_requests(request):

    challenges = Challenge.objects.filter(status = 'accepted')
    context = {
        'challenges': challenges
    }
    return render(request, 'matches/match_requests.html', context)


def scheduled_matches(request):

    challenges = Challenge.objects.filter(status = 'scheduled')
    context = {
        'challenges': challenges
    }
    return render(request, 'matches/scheduled_matches.html', context)


class AccountNames(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        data = [12, 19, 3, 5, 2, 3]
        # usernames = [user.username for user in User.objects.all()]
        data = {
                "data": data,
                "labels": labels,
            }
        return Response(data)

class AccountPointsHistory(APIView):
    def get(self, request, format=None):
        player = Participant.objects.filter(player = Account.objects.get(user = request.user))
        data = [1000]
        x = 0
        match_time = [x]
        for p in player:
            data.append(p.player_new_ratings)
            match_time.append(x)
            x += 1
        data = {
            'data': data, 
            'time': match_time
        }

        return Response(data)

class GetAllPlayers(APIView):
    def get(self, request, format=None):
        accounts = Account.objects.all().order_by('user__username')
        players_list = []
        for account in accounts:
            if not account.user == request.user:
                players_list.append((account.name, account.user.username))
        
        data = {
            'data': players_list
        }

        return Response(data)
