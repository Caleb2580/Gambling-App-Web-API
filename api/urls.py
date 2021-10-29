from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('balance/', views.balance, name="balance"),
    path('crash/', views.crash, name="crash"),
    path('crash_bet/', views.crash_bet, name="crash_bet"),
    path('crash_cashout/', views.crash_cashout, name="crash_cashout"),
    path('deposit/', views.deposit, name="deposit"),
    path('crash_players/', views.crash_players, name="crash_players"),
]

















