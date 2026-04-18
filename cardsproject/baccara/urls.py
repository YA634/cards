from django.urls import path
# from django.contrib.auth.views import baccara_view
from .import views

app_name = 'baccara'

urlpatterns = [
    path('home/',views.baccara_view, name='home')
]