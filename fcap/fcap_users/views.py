from django.shortcuts import render, redirect
from django.views import View
import json 
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.models import User
from .forms import AccountForm, UserForm
from django.contrib.auth import authenticate, login, logout
from .models import Account
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def index(request): 
    return render(request, 'index.html')

def loginPage(request): 
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
        
