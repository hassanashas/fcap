from django.urls import path

from .views import views
from .views import challenges_views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('matches', views.index, name='index'),
    path('login', views.loginPage, name='login'),
    path('register', views.register, name='register'),
    path('add_match', views.add_match, name='add_match'),
    path('all_members', views.all_members, name='all_members'),
    path('match_requests', views.match_requests, name='match_requests'),
    path('schedule/<str:pk>', challenges_views.schedule_challenge, name='schedule_challenge'),
    path('scheduled_matches', views.scheduled_matches, name='scheduled_matches'),
    path('add_challenge_match/<str:pk>', challenges_views.add_challenge_match, name='add_challenge_match'),
    path('rankings', views.rankings, name='rankings'),
    path('challenges', challenges_views.challenges, name ='challenges'),
    path('challenges/<str:pk>', challenges_views.get_challenge, name='get_challenge'),
    path('new_challenge', challenges_views.add_new_challenge, name='add_new_challenge'),
    path('challenge_requests', challenges_views.challenge_requests, name='challenge_requests'),
    path('validate_email', csrf_exempt(views.EmailVerification.as_view()), name='validate_email'),
    path('validate_username', csrf_exempt(views.UsernameVerification.as_view()), name='validate_username'),
    path('validate_name', csrf_exempt(views.NameVerification.as_view()), name='validate_name'),
    path('api/data', views.getData, name='api-data'),
    path('api/chart/data', views.AccountNames.as_view()),
    path('api/users/points_history', views.AccountPointsHistory.as_view()),
    path('api/users/get_accounts', views.GetAllPlayers.as_view()),
    # path('api/users/get_player_challenges', challenges_views.GetPlayerChallenges.as_view()),
    path('logout', views.logoutUser, name='logout'),
]
