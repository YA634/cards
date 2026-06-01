from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cards.urls')),
    path('baccara/',include('baccara.urls')),
    path('blackjack/',include('blackjack.urls')),
    path('poker/',include('poker.urls')),
    path('accounts/',include('accounts.urls')),
    # path('cards/',include('cards.urls')),
]
