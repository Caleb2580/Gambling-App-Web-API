from django.db import models
import random
from time import sleep
import time

# Create your models here.


def get_crash():
    x = random.uniform(0, 1)
    multiplier = .99 / (1-x)
    if multiplier < 1.0:
        return 1.0
    return round(multiplier, 2)


def get_end_time(mul):
    i = 1.00
    start_time = time.time()
    total_sleep_time = 0
    while i <= mul:
        i += .01
        amount_to_sleep = .2 / (i ** 1.00000000001)
        total_sleep_time += amount_to_sleep
    return start_time + total_sleep_time


class Players(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Player(models.Model):
    players = models.ForeignKey(Players, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=300)
    balance = models.FloatField()
    computer_name = models.CharField(max_length=300, default='')

    def __str__(self):
        return str(self.player_name) + " " + str(self.computer_name) + " " + str(self.balance)


class Crash(models.Model):
    multiplier = models.FloatField(default=1.00)
    start_time = models.FloatField(default=.00)
    end_time = models.FloatField(default=.00)

    def __str__(self):
        return str(self.multiplier)


class CrashPlayer(models.Model):
    crash_game = models.ForeignKey(Crash, on_delete=models.CASCADE)
    bet = models.FloatField(default=0.0)
    cashout = models.FloatField(default=0.0)
    player_name = models.CharField(max_length=300, default='')
    computer_name = models.CharField(max_length=300, default='')

    def __str__(self):
        return str(self.player_name)


























