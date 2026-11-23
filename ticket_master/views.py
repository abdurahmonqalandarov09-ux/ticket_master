from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q, Count
from .models import *
from django.contrib.auth.models import User


def home_page(request):
    if request.method == 'GET':
        st = Match.objects.filter(status='upcoming').order_by('date')[:6]
    return render(request, 'home.html', {'st': st})


def registration(request):
    if request.method == 'POST':
        data = request.POST
        if User.objects.filter(username=data['username']).exists():
            messages.error(request, "Такой логин уже занят")
            return render(request, 'registration.html')
        User.objects.create_user(
            username = data['username'],
            password = data['password']
        )
        return redirect('home')
    return render(request, 'registration.html')




def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(request, username = data['username'], password = data['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверный логин или пароль")
    return render(request, 'login_user.html')



@login_required
def logout_user(request):
    logout(request)
    return redirect('login')




def matches(request):
    match_list = Match.objects.all().order_by('date')

    league_id = request.GET.get('league')      
    if league_id:
        match_list = match_list.filter(league_id=league_id)

    return render(request, 'matches.html', {
        'matches': match_list,
        'leagues': Leagues.objects.all(),      
        'league': league_id,                   
    })


def match_detail(request, id):
    match = get_object_or_404(Match, id = id)
    ticket_types = match.tickettype_set.all()
    return render(request, 'match_detail.html', {'match': match, 'ticket_types': ticket_types})



@login_required
def buy_ticket(request, id):
    ticket_type = get_object_or_404(TicketType, id=id)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])           

        if quantity < 1 or quantity > ticket_type.quantity:   
            return redirect('match_detail', id=ticket_type.match.id)

        ticket_type.quantity = ticket_type.quantity - quantity   
        ticket_type.save()                                       

        Orders.objects.create(
            user=request.user,
            ticket_type=ticket_type,
            quantity=quantity,
            price=ticket_type.price * quantity,
            status='paid',
        )
        messages.success(request, 'Билеты куплены')
        return redirect('match_detail', id=ticket_type.match.id)
    return render(request, 'buy_ticket.html', {'ticket_type': ticket_type})




@login_required
def my_orders(request):
    orders = request.user.orders.order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})





def teams(request):
    team_list = Teams.objects.all().order_by('team_name')
    league_id = request.GET.get('league')
    if league_id:
        team_list = team_list.filter(leagues=league_id)
    return render(request, 'teams.html', {
        'teams': team_list,
        'leagues': Leagues.objects.all(),
        'league': league_id,
    })



def team_detail(request, id):
    team = get_object_or_404(Teams, id=id)
    players = team.players.all().order_by('number')
    return render(request, 'team_detail.html', {'team': team, 'players': players})




def player_detail(request, id):
    player = get_object_or_404(Players, id=id)
    return render(request, 'player_detail.html', {'player': player})





def leagues(request):
    return render(request, 'leagues.html', {'leagues': Leagues.objects.all()})




def league_detail(request, id):
    league = get_object_or_404(Leagues, id=id)
    teams = league.teams.all()
    league_matches = league.match_set.order_by('date')
    return render(request, 'league_detail.html', {
        'league': league,
        'teams': teams,
        'matches': league_matches,
    })



def stadiums(request):
    return render(request, 'stadiums.html', {'stadiums': Stadium.objects.all()})




def stadium_detail(request, id):
    stadium = get_object_or_404(Stadium, id=id)
    return render(request, 'stadium_detail.html', {'stadium': stadium, 'teams': stadium.teams.all()})




def upcoming_matches(request):
    matches = Match.objects.filter(
        status = 'upcoming'
    ).order_by('date')
    return render(request, 'past_matches.html', {'matches': matches})



def past_matches(request):
    matches = Match.objects.filter(
        status='finished'
    ).order_by('-date')

    return render(request, 'past_matches.html', {
        'matches': matches
    })


def match_video(request, id):
    match = get_object_or_404(Match,id=id,status='finished')
    return render(request, 'match_video.html', {'match': match})



@login_required
def my_tickets(request):
    orders = Orders.objects.filter(
        user=request.user,
        status='paid'
    ).order_by('-created_at')

    return render(request, 'my_tickets.html', {'orders': orders})