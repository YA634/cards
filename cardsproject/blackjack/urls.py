from django.urls import path
# from django.contrib.auth.views import baccara_view
from .import views

app_name = 'blackjack'

urlpatterns = [
    path('home/',views.blackjack_view, name='home'),
    path('bj1/',views.bj1_view, name='bj1'),
    path('bj2/',views.bj2_view, name='bj2'),
    path('bj3/',views.bj3_view, name='bj3'),
    path('result/',views.result_view, name='result'),
]