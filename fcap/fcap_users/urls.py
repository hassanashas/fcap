from django.urls import path

from fcap.fcap_users.views.challenges_views import challenge 
from .views import views
from .views import challenges_views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('matches', views.index, name='index'),
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('add_match', views.add_match, name='add_match'),
    path('rankings', views.rankings, name='rankings'),
    path('validate_email', csrf_exempt(views.EmailVerification.as_view()), name='validate_email'),
    path('validate_username', csrf_exempt(views.UsernameVerification.as_view()), name='validate_username'),
    path('validate_name', csrf_exempt(views.NameVerification.as_view()), name='validate_name'),
    path('api/data', views.getData, name='api-data'),
    path('api/chart/data', views.AccountNames.as_view()),
    path('api/users/points_history', views.AccountPointsHistory.as_view()),
    path('logout', views.logoutUser, name='logout'),
]
