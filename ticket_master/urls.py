from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('matches/', views.matches, name='matches'),
    path('matches/<int:id>/', views.match_detail, name='match_detail'),
    path('matches/upcoming/', views.upcoming_matches, name='upcoming_matches'),
    path('matches/past/', views.past_matches, name='past_matches'),
    path('matches/<int:id>/video/', views.match_video, name='match_video'),
    path('tickets/buy/<int:id>/', views.buy_ticket, name='buy_ticket'),
    path('tickets/my/', views.my_tickets, name='my_tickets'),
    path('orders/', views.my_orders, name='my_orders'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:id>/', views.team_detail, name='team_detail'),
    path('players/<int:id>/', views.player_detail, name='player_detail'),
    path('leagues/', views.leagues, name='leagues'),
    path('leagues/<int:id>/', views.league_detail, name='league_detail'),
    path('stadiums/', views.stadiums, name='stadiums'),
    path('stadiums/<int:id>/', views.stadium_detail, name='stadium_detail'),
]
