from django.db import transaction

@transaction.atomic
def update_user_money(user, amount):
    user.money += amount
    user.save()
    return user.money

def can_bet(user, bet_amount):
    return user.money >= bet_amount