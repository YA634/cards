from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from cards_all.card import Trump_card
from cards_all.blackjack import Blackjack
from accounts.utils import update_user_money, can_bet
import copy
from django.contrib.auth.decorators import login_required
# from .utils import get_roadmap_display,update_roadmap

@login_required
def blackjack_view(request):
    request.session['process_end'] = 0
    bet_amount = 0
    bet_on = None
    # winner = None
    # result = None
    # d_sum = None
    # p_sum= None
    # d_sum2 = None
    # p_sum2 = None
    error_mes = None
    if request.method == 'POST':
        bet_amount = int(request.POST.get('bet_amount'))
        if can_bet(request.user, bet_amount) == False:
            error_mes = '所持金が足りません'
            return render(request,'blackjack_home.html',{'bet_amount':bet_amount, 'bet_on':bet_on, 'error_mes':error_mes})
        else:
            update_user_money(request.user, -bet_amount)
            bet_on = request.POST.get('bet_on')
            request.session['bet_on'] = bet_on
            request.session['bet_amount'] = bet_amount
            return redirect('blackjack:bj1')
        # p_d3 = []
        # d_d3 = []
    return render(request,'blackjack_home.html',{'bet_amount':bet_amount, 'bet_on':bet_on, 'error_mes':error_mes})

def bj1_view(request):
    first_d_cards = []
    first_p_cards = []
    cards_li = []
    request.session['ex_turn_result1'] = None
    request.session['ex_turn_result2'] = None
    blackjack = Blackjack(cards_li)
    card = Trump_card()
    first_d_cards = [card.drow(),card.drow()]
    # first_p_cards = [card.drow(),card.drow()]
    first_p_cards = ['heart_5','spade_5']
    request.session['cards_li'] = blackjack.cards_li
    request.session['first_d_c'] = first_d_cards
    request.session['first_p_c'] = first_p_cards
    p_p = blackjack.pc(first_p_cards)
    ex_acs = blackjack.ex_ac(first_d_cards,first_p_cards)
    # if request.method == 'POST':
    #     ex_ac = request.POST.get('ex_acs')
    # request.session['ex_ac'] = ex_ac
    return render(request,'bj1.html',{'first_d_cards':first_d_cards,'first_p_cards':first_p_cards,'ex_acs':ex_acs,'p_p':p_p})

def bj2_view(request):
    ex_p_card = None
    if request.method == 'POST':
        ex_ac = request.POST.get('ex_acs')
    request.session['ex_ac'] = ex_ac
    dli = request.session.get('first_d_c')
    pli = request.session.get('first_p_c')
    cards_li = request.session.get('cards_li')
    blackjack = Blackjack(cards_li)
    blackjack.process_end = request.session.get('process_end')
    acs = blackjack.acs
    # if ex_ac == 'no' or ex_ac == 'インシュアランス' or ex_ac == 'スプリッティングペアー':
    #     acs = blackjack.acs
    #     # if request.method == 'POST':
    #     #     ac = request.POST.get('ac')
    #     #     blackjack.normal_faze(ac)
    # else:
    #     result = blackjack.ex_faze(dli, pli, 1, ex_ac)
    ex_turn_result = blackjack.ex_faze(dli, pli, 1, ex_ac)
    request.session['ex_turn_result'] = ex_turn_result
    request.session['process_end'] = blackjack.process_end
    pli = ex_turn_result['pli']
    request.session['first_p_c'] = pli
    p_p = blackjack.pc(pli)
    return render(request,'bj2.html',{'acs':acs,'ex_ac':ex_ac,'dli':dli,'pli':pli,'ex_p_card':ex_p_card,'p_p':p_p,'ex_turn_result':ex_turn_result,})

def bj3_view(request):
    dli = request.session.get('first_d_c')
    pli = request.session.get('first_p_c')
    cards_li = request.session.get('cards_li')
    ex_ac = request.session.get('ex_ac')
    ex_turn_result = request.session.get('ex_turn_result')
    blackjack = Blackjack(cards_li)
    blackjack.process_end = request.session.get('process_end')
    if request.method == 'POST':
        acs = blackjack.acs
        ac = request.POST.get('acs')
        ex_p_cards = []
        ex_p_card = blackjack.normal_faze(ac)
        ex_p_cards.append(ex_p_card)
        if ex_p_card != None:
            pli2 = pli.copy()
            pli2.append(ex_p_card)
            p_p = blackjack.pc(pli2)
            request.session['first_p_c'] = pli2
            if p_p > 21:
                if ex_turn_result['process_end'] == 100:
                    return redirect('blackjack:result')
                elif ex_turn_result['process_end'] == 2:
                    request.session['ex_turn_result2'] = ex_turn_result
                    return redirect('blackjack:result')
                else:
                    request.session['ex_turn_result1'] = ex_turn_result
                    ex_turn_result = blackjack.ex_faze(dli, pli, 1, ex_ac)
                    request.session['ex_turn_result'] = ex_turn_result
                    pli = ex_turn_result['pli']
                    request.session['first_p_c'] = pli
                    p_p = blackjack.pc(pli)
                    return render(request,'bj2.html',{'acs':acs,'ex_ac':ex_ac,'ex_p_card':ex_p_card,'ex_p_cards':ex_p_cards,'dli':dli,'pli':pli,'p_p':p_p,'ex_turn_result':ex_turn_result})
            return render(request,'bj2.html',{'acs':acs,'ex_ac':ex_ac,'ex_p_card':ex_p_card,'ex_p_cards':ex_p_cards,'dli':dli,'pli':pli,'p_p':p_p,'ex_turn_result':ex_turn_result})
        else:
            print(ex_p_card)
            print(ex_turn_result['process_end'])
            p_p = blackjack.pc(pli)
            if ex_turn_result['process_end'] == 100:
                return redirect('blackjack:result')
            elif ex_turn_result['process_end'] == 2:
                request.session['ex_turn_result2'] = ex_turn_result
                return redirect('blackjack:result')
            else:
                request.session['ex_turn_result1'] = ex_turn_result
                new_ex_turn_result = blackjack.ex_faze(dli, pli, 1, ex_ac)
                request.session['process_end'] = blackjack.process_end
                request.session['ex_turn_result'] = new_ex_turn_result
                print(new_ex_turn_result)
                return render(request,'bj2.html',{'acs':acs,'ex_ac':ex_ac,'ex_p_card':ex_p_card,'dli':dli,'pli':pli,'p_p':p_p,'ex_turn_result':new_ex_turn_result})

def result_view(request):
    dli = request.session.get('first_d_c')
    pli = request.session.get('first_p_c')
    dli2 = dli.copy()
    cards_li = request.session.get('cards_li')
    ex_ac = request.session.get('ex_ac')
    bet_amount = request.session.get('bet_amount')
    ex_turn_result = request.session.get('ex_turn_result')

    blackjack = Blackjack(cards_li)
    result1 = blackjack.d_ef(dli2,pli)
    result2 = blackjack.lc(request.user, pli, bet_amount, result1['dp'])
    ex_turn_result1 = request.session.get('ex_turn_result1')
    ex_turn_result2 = request.session.get('ex_turn_result2')
    
    return render(request,'result.html',{'ex_ac':ex_ac,'dli':dli,'pli':pli,'result1':result1,'result2':result2,'ex_turn_result1':ex_turn_result1,'ex_turn_result2':ex_turn_result2})
