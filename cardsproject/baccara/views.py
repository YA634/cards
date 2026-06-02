from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from cards_all.card import Trump_card
from cards_all.baccara import Baccara
from accounts.utils import update_user_money, can_bet
from .utils import get_roadmap_display,update_roadmap
from django.contrib.auth.decorators import login_required
# from baccara import Baccara
# Create your views here.

@login_required
def baccara_view(request):
    bet_amount = None
    bet_on = None
    first_b_cards = []
    first_p_cards = []
    ex_drow = {'p_card': None, 'b_card': None}
    winner = None
    result = None
    b_sum = None
    p_sum= None
    b_sum2 = None
    p_sum2 = None
    error_mes = None
    roadmap_data = get_roadmap_display(request.user)
    # baccara = Baccara()
    if request.method == 'POST':
        bet_amount = int(request.POST.get('bet_amount'))
        if can_bet(request.user, bet_amount) == False:
            error_mes = '所持金が足りません'
            return render(request,'baccara_home.html',{'first_b_cards':first_b_cards, 'first_p_cards':first_p_cards, 'p_sum':p_sum, 'b_sum':b_sum, 'p_sum2':p_sum2, 'b_sum2':b_sum2, 'bet_amount':bet_amount, 'bet_on':bet_on, 'ex_drow':ex_drow, 'winner':winner, 'result':result, 'error_mes':error_mes})
        else:
            update_user_money(request.user, -bet_amount)
        bet_on = request.POST.get('bet_on')
        baccara = Baccara()
        card = Trump_card()
        first_b_cards = [card.drow(),card.drow()]
        first_p_cards = [card.drow(),card.drow()]
        fli = [first_p_cards[0],first_p_cards[1],first_b_cards[0],first_b_cards[1]]
        p_sum = baccara.p_cul(card.cards_dc[fli[0]], card.cards_dc[fli[1]])
        b_sum = baccara.p_cul(card.cards_dc[fli[2]], card.cards_dc[fli[3]])
        p_d3 = None
        b_d3 = None
        if p_sum < 6:
            if b_sum < 8:
                p_d3 = card.drow()
                print(f"プレイヤーのドローカード {p_d3}")
                p_sum2 = baccara.p_cul(p_sum, card.cards_dc[p_d3])
                print(f"プレイヤーの点数 {p_sum2}")
                p_d3_n = card.cards_dc[p_d3]
                if b_sum < 3 or (b_sum == 3 and not(p_d3_n == 8)) or (b_sum == 4 and (p_d3_n not in [10, 1, 8, 9])) or (b_sum == 5 and (p_d3_n in [4, 5, 6, 7])) or (b_sum == 6 and (p_d3_n in [6, 7])):
                    b_d3 = card.drow()
                    print(f"バンカーのドローカード {b_d3}")
                    b_sum2 = baccara.p_cul(b_sum, card.cards_dc[b_d3])
                    print(f"バンカーの点数 {b_sum2}")
                else:
                    b_sum2 = b_sum
        elif p_sum < 8:
            if b_sum < 6:
                b_d3 = card.drow()
                print(f"バンカーのドローカード {b_d3}")
                b_sum2 = baccara.p_cul(b_sum, card.cards_dc[b_d3])
                print(f"バンカーの点数 {b_sum2}")
                p_sum2 = p_sum
            else:
                b_sum2 = b_sum
                p_sum2 = p_sum
        else:
            b_sum2 = b_sum
            p_sum2 = p_sum
        
        if p_sum2 == None:
            p_sum2 = p_sum
        if b_sum2 == None:
            b_sum2 = b_sum
        if p_sum2 > b_sum2:
            winner = "player"
        elif p_sum2 < b_sum2:
            winner = "banker"
        else:
            winner = "tie"
        if winner == bet_on:
            if winner == "引き分け":
                amount = bet_amount*9
                result = f'勝ち {amount}円get'
            else:
                amount = bet_amount*2
                result = f'勝ち {amount}円get'
        else:
            amount = 0
            result = f'負け {bet_amount}円lost'
        update_user_money(request.user, amount)
        ex_drow = {'p_card':p_d3,'b_card':b_d3}
        print(bet_on)
        print(result)
        update_roadmap(request.user,winner)
        roadmap_data = get_roadmap_display(request.user)



    return render(request,'baccara_home.html',{'first_b_cards':first_b_cards, 'first_p_cards':first_p_cards, 'p_sum':p_sum, 'b_sum':b_sum, 'p_sum2':p_sum2, 'b_sum2':b_sum2, 'bet_amount':bet_amount, 'bet_on':bet_on, 'ex_drow':ex_drow, 'winner':winner, 'result':result, 'error_mes':error_mes, 'roadmap_data':roadmap_data})
