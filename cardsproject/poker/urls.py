from django.urls import path
# from django.contrib.auth.views import baccara_view
from .import views

app_name = 'poker'

urlpatterns = [
  path('home/',views.poker_view, name='home'),
]