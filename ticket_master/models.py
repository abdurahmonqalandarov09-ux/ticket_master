from django.db import models
from django.conf import settings


class Leagues(models.Model):
    league_name = models.CharField(max_length=120)
    country = models.CharField(max_length=80, blank=True)
    league_logo = models.ImageField(upload_to='leagues/', null=True, blank=True)

    def __str__(self):
        return self.league_name


class Stadium(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='stadiums/', null=True, blank=True)

    def __str__(self):
        return self.name


class Coaches(models.Model):
    coach_name = models.CharField(max_length=120)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=120)
    photo = models.ImageField(upload_to='coaches/', null=True, blank=True)

    def __str__(self):
        return self.coach_name


class Teams(models.Model):
    team_name = models.CharField(max_length=120)
    team_logo = models.ImageField(upload_to='teams/', null=True, blank=True)
    country = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=100, blank=True)
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)
    coach = models.OneToOneField(Coaches, on_delete=models.SET_NULL, null=True, blank=True, related_name='team')
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
    leagues = models.ManyToManyField(Leagues, related_name='teams')

    def __str__(self):
        return self.team_name


class Players(models.Model):
    POSITIONS = [
        ('gk', 'Goalkeeper'),
        ('cb', 'Centre Back'),
        ('lb', 'Left Back'),
        ('rb', 'Right Back'),
        ('cdm', 'Central Defending Midfielder'),
        ('cm', 'Central Midfielder'),
        ('cam', 'Central Attacking Midfielder'),
        ('lm', 'Left Midfielder'),
        ('rm', 'Right Midfielder'),
        ('lw', 'Left Winger'),
        ('rw', 'Right Winger'),
        ('ss', 'Second Striker'),
        ('st', 'Striker'),
    ]
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='players')
    player_name = models.CharField(max_length=120)
    position = models.CharField(max_length=3, choices=POSITIONS)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=80, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    transfer_value = models.PositiveBigIntegerField(default=0)
    is_captain = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='players/', null=True, blank=True)

    def __str__(self):
        return self.player_name




class Match(models.Model):
    STATUS = [
        ('upcoming', 'Предстоящий'),
        ('finished', 'Законченный')
    ]

    league = models.ForeignKey(Leagues, on_delete=models.CASCADE, null=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True, blank=True)
    team1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='home_team', null=True)
    team2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='away_team', null=True)
    home_score = models.PositiveIntegerField(null=True, blank=True)
    away_score = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=120, choices=STATUS, default='upcoming')
    video_file = models.FileField(upload_to='videos/', blank=True)



    def __str__(self):
        return f"{self.team1} - {self.team2}"





class TicketType(models.Model):
    TYPE = [
        ('vip', 'VIP'),
        ('usual', 'Обычный')
    ]
    quantity = models.PositiveBigIntegerField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    ticket = models.CharField(max_length=120, choices=TYPE, default='usual')


    def __str__(self):
        return f"Заказ №{self.id} - {self.user}"







class Orders(models.Model):
    STATUS = [
        ('paid', 'Оплаченный'),
        ('canceled', 'Отменен')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=120, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.user
