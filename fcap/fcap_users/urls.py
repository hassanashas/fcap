from django.urls import path 
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('add_match', views.add_match, name='add_match'),
    path('validate_email', csrf_exempt(views.EmailVerification.as_view()), name='validate_email'),
    path('validate_username', csrf_exempt(views.UsernameVerification.as_view()), name='validate_username'),
    path('validate_name', csrf_exempt(views.NameVerification.as_view()), name='validate_name'),
    path('logout', views.logoutUser, name='logout'),
]
