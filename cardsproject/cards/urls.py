from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('baccara/',include('baccara.urls')),
    path('blackjack/',include('blackjack.urls')),
]