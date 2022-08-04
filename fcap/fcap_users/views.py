from django.shortcuts import render
from django.views import View
import json 
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def index(request): 
    return render(request, 'index.html')

def login(request): 
    return render(request, 'user/login.html')

def register(request): 
    return render(request, 'user/register.html')

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
        
