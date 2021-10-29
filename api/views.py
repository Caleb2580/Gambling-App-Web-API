from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Players, Player, Crash, CrashPlayer
from django.core import serializers
import json
from time import sleep
import time
import random


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


# Create your views here.

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("<h1>Caleb's gambling api<h1>")
    else:
        return JsonResponse({'error': 'method not allowed'})


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return JsonResponse({'error': 'method not allowed'})
    else:
        req = dict(request.POST)
        if 'computer_name' in req:
            players_pre_serialize = Players.objects.get(name="player_list").player_set.filter()
            players_raw = json.loads(serializers.serialize('json', players_pre_serialize))
            for entry in players_raw:
                computer_name = entry['fields']['computer_name']
                if req['computer_name'][0] == computer_name:
                    player = Players.objects.get(name='player_list').player_set.get(computer_name=computer_name)
                    if None != req['username'][0] != '':
                        player.player_name = req['username'][0]
                        print(player.player_name)
                        player.save()
                    return JsonResponse({'success': True, 'username': player.player_name, 'balance': player.balance})
            players = Players.objects.get(name="player_list")
            players.player_set.create(player_name=req['username'][0], computer_name=req['computer_name'][0], balance=0.0)
            players.save()
            return JsonResponse({'success': True, 'username': req['username'][0], 'balance': 0.0})
        else:
            return JsonResponse({'success': False})


@csrf_exempt
def balance(request):
    if request.method == 'GET':
        return JsonResponse({'error': 'method not allowed'})
    else:
        req = dict(request.POST)
        if 'computer_name' in req:
            players_pre_serialize = Players.objects.get(name="player_list").player_set.filter()
            players_raw = json.loads(serializers.serialize('json', players_pre_serialize))
            for entry in players_raw:
                computer_name = entry['fields']['computer_name']
                if req['computer_name'][0] == computer_name:
                    player = Players.objects.get(name='player_list').player_set.get(computer_name=computer_name)
                    return JsonResponse({'success': True, 'balance': player.balance})
            return JsonResponse({'success': True, 'balance': 0})
        return JsonResponse({'success': False, 'error': 'Not logged in'})


@csrf_exempt
def crash(request):
    if request.method == 'GET':
        crash_model = Crash.objects.get(id=1)
        if time.time() < crash_model.start_time:
            return JsonResponse({'running': False, 'start_time': crash_model.start_time, 'multiplier': crash_model.multiplier, 'done': False})
        elif crash_model.end_time > time.time() > crash_model.start_time:
            return JsonResponse({'running': True, 'start_time': crash_model.start_time, 'multiplier': crash_model.multiplier, 'done': False})
        elif crash_model.start_time < time.time() > crash_model.end_time + 3:
            players = Players.objects.get(name='player_list')
            crash_players_pre_serialize = crash_model.crashplayer_set.filter()
            crash_players_raw = json.loads(serializers.serialize('json', crash_players_pre_serialize))
            players_pre_serialize = Players.objects.get(name="player_list").player_set.filter()
            players_raw = json.loads(serializers.serialize('json', players_pre_serialize))

            for ent in crash_players_raw:
                comp_name = ent['fields']['computer_name']
                # bet = ent['fields']['bet']
                # cashout = ent['fields']['cashout']
                # for entry in players_raw:
                #     computer_name = entry['fields']['computer_name']
                #     if comp_name == computer_name:
                #         win = cashout * bet
                #         print('won', win)
                #         player = Players.objects.get(name='player_list').player_set.get(computer_name=computer_name)
                #         player.balance += win
                #         player.save()
                crash_model.crashplayer_set.get(computer_name=comp_name).delete()

            new_mult = get_crash()
            new_end = get_end_time(new_mult)
            crash_model.end_time = new_end + 10
            crash_model.start_time = time.time() + 10
            crash_model.multiplier = new_mult
            crash_model.save()
            print(crash_model)
            return JsonResponse({'running': False, 'done': True})
        elif crash_model.start_time < time.time() > crash_model.end_time:
            return JsonResponse({'running': False, 'done': True})
        return JsonResponse({'error': 'Something went wrong'})
    else:
        return JsonResponse({'error': 'method not allowed'})


@csrf_exempt
def crash_bet(request):
    if request.method == 'GET':
        return JsonResponse({'error': 'method not allowed'})
    else:
        req = dict(request.POST)
        crash_model = Crash.objects.get(id=1)
        if time.time() < crash_model.start_time:
            if 'computer_name' in req:
                players_pre_serialize = Players.objects.get(name="player_list").player_set.filter()
                players_raw = json.loads(serializers.serialize('json', players_pre_serialize))
                crash_players_pre_serialize = crash_model.crashplayer_set.filter()
                crash_players_raw = json.loads(serializers.serialize('json', crash_players_pre_serialize))
                for entry in players_raw:
                    computer_name = entry['fields']['computer_name']
                    if req['computer_name'][0] == computer_name:
                        for ent in crash_players_raw:
                            comp_name = ent['fields']['computer_name']
                            if comp_name == computer_name:
                                return JsonResponse({'success': False, 'error': 'already bet'})
                        crash_model.crashplayer_set.create(bet=float(req['bet'][0]), cashout=2.0, player_name=entry['fields']['player_name'], computer_name=req['computer_name'][0])
                        # print('set', crash_model.crashplayer_set.all())
                        player = Players.objects.get(name='player_list').player_set.get(computer_name=computer_name)
                        if player.balance >= float(req['bet'][0]):
                            player.balance -= float(req['bet'][0])
                            player.save()

                            return JsonResponse({'success': True, 'balance': player.balance})
                        else:
                            return JsonResponse({'success': False, 'error': "Don't have enough"})
            return JsonResponse({'success': False, 'error': 'Not logged in'})
        else:
            return JsonResponse({'success': False})


@csrf_exempt
def crash_cashout(request):
    if request.method == 'GET':
        return JsonResponse({'error': 'method not allowed'})
    else:
        req = dict(request.POST)
        multiplier = float(req['multiplier'][0])
        crash_model = Crash.objects.get(id=1)
        crash_players_pre_serialize = crash_model.crashplayer_set.filter()
        crash_players_raw = json.loads(serializers.serialize('json', crash_players_pre_serialize))
        for ent in crash_players_raw:
            if req['computer_name'][0] == ent['fields']['computer_name']:
                computer_name = ent['fields']['computer_name']
                player_player = Players.objects.get(name='player_list').player_set.get(computer_name=computer_name)
                crash_player = Crash.objects.get(id=1).crashplayer_set.get(computer_name=computer_name)
                crash_player.cashout = multiplier
                player_player.balance += crash_player.bet * crash_player.cashout
                crash_player.save()
                player_player.save()
                return JsonResponse({'success': True, 'balance': player_player.balance})

        return JsonResponse({'success': False, 'error': 'did not bet'})


@csrf_exempt
def deposit(request):
    if request.method == 'GET':
        return JsonResponse({'error': 'method not allowed'})
    else:
        req = dict(request.POST)
        try:
            player = Players.objects.get(name='player_list').player_set.get(computer_name=req['computer_name'][0])
            player.balance += round(float(req['amount'][0]), 2)
            player.save()
            return JsonResponse({'success': True})
        except:
            return JsonResponse({'error': 'method not allowed'})






