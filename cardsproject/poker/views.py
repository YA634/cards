from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from cards_all.card import Trump_card
from cards_all.poker import Poker
from accounts.utils import update_user_money, can_bet
import copy
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def poker_view(request):
    request.session['process_end'] = 0
    mem_amount = 0
    # winner = None
    # result = None
    # d_sum = None
    # p_sum= None
    # d_sum2 = None
    # p_sum2 = None
    error_mes = None
    if request.method == 'POST':
      mem_amount = int(request.POST.get('mem_amount'))
      request.session['mem_amount'] = mem_amount
      # return redirect('poker:pk1')

    # return render(request,'poker_home.html',{'mem_amount':mem_amount,'error_mes':error_mes})
    return render(request, 'mikan.html')

def pk1_view(request):
   return render()