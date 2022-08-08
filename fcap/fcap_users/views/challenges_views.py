
from django.shortcuts import render, redirect
from django.views import View

def challenge(request):
    return render('challenge.html')