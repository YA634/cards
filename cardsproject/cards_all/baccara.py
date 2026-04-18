from cards_all.card import Trump_card
import time


class Baccara():   

    def __init__(self):
        self.card = Trump_card()
        self.cards_dc = self.card.cards_dc
        self.cards_li = self.card.cards_li
        # self.players_all = player

    def step0(self):
        self.p_d1 = self.card.drow()
        self.p_d2 = self.card.drow()
        self.b_d1 = self.card.drow()
        self.b_d2 = self.card.drow()
        # self.p_d1 = "♡ace"
        # self.p_d2 = "♡2"
        # self.b_d1 = "♡5"
        # self.b_d2 = "♤ace"
        return [self.p_d1, self.p_d2, self.b_d1, self.b_d2]
    
    def p_cul(self, d1, d2):
        self.sum = d1 + d2
        if self.sum >= 10:
            if self.sum >= 20:
                self.sum -= 20
            else:
                self.sum -= 10
        return self.sum

    def df(self, p_sum, b_sum):
        if p_sum < 6:
            if b_sum < 8:
                p_d3 = self.card.drow()
                print(f"プレイヤーのドローカード {p_d3}")
                p_sum = self.p_cul(p_sum, self.cards_dc[p_d3])
                print(f"プレイヤーの点数 {p_sum}")
                time.sleep(1)
                p_d3_n = self.cards_dc[p_d3]
                if b_sum < 3 or (b_sum == 3 and not(p_d3_n == 8)) or (b_sum == 4 and (p_d3_n not in [10, 1, 8, 9])) or (b_sum == 5 and (p_d3_n in [4, 5, 6, 7])) or (b_sum == 6 and (p_d3_n in [6, 7])):
                    b_d3 = self.card.drow()
                    print(f"バンカーのドローカード {b_d3}")
                    b_sum = self.p_cul(b_sum, self.cards_dc[b_d3])
                    print(f"バンカーの点数 {b_sum}")
        elif p_sum < 8:
            if b_sum < 6:
                b_d3 = self.card.drow()
                print(f"バンカーのドローカード {b_d3}")
                b_sum = self.p_cul(b_sum, self.cards_dc[b_d3])
                print(f"バンカーの点数 {b_sum}")
        return [p_sum, b_sum]

    def ef(self, p_sum, b_sum, pa1, pa2):
        time.sleep(1)
        print(f"プレイヤーの合計点{p_sum}, バンカーの合計点{b_sum}")
        if p_sum > b_sum:
            self.winner = "プレイヤー"
        elif p_sum < b_sum:
            self.winner = "バンカー"
        else:
            self.winner = "引き分け"

        self.m_in_or_de = 0
        if self.winner == "引き分け":
            print(f"{self.winner}")
            if pa1 == self.winner or pa1 == "3":
                self.m_in_or_de = pa2*9
                print(f"あなたの勝ち 賞金{pa2*9}円")
            else:
                self.m_in_or_de = 0
                print(f"あなたの負け {pa2}円lost")
        elif self.winner == "プレイヤー":
            print(f"勝者は{self.winner}")
            if pa1 == self.winner or pa1 == "1":
                self.m_in_or_de = pa2*2
                print(f"あなたの勝ち 賞金{pa2*2}円")
            else:
                self.m_in_or_de = 0
                print(f"あなたの負け {pa2}円lost")
        else:
            print(f"勝者は{self.winner}")
            if pa1 == self.winner or pa1 == "2":
                self.m_in_or_de = pa2*2
                print(f"あなたの勝ち 賞金{pa2*2}円")
            else:
                self.m_in_or_de = 0
                print(f"あなたの負け {pa2}円lost")
        self.player1.money += self.m_in_or_de
        print(f"あなたの所持金は{self.player1.money}円です")

        
    def start(self):
        x = 0
        while x < 1:
            x1 = 0
            # self.p_name = input()
            while x1 < 1:
                self.pa1 = input("プレイヤー(1)、バンカー(2)、引き分け(3),どれに賭ける？")
                if self.pa1 == "プレイヤー" or self.pa1 == "バンカー" or self.pa1 == "引き分け" or self.pa1 == "1" or self.pa1 == "2" or self.pa1 == "3":
                    x1 += 1
            # self.player1 = self.players_all[0]
            self.l_out = 0
            while self.l_out < 1:
                self.pa2 = int(input(f"賭ける金額を入力... プレイヤー1の残額{self.player1.money}"))
                if self.pa2 <= self.player1.money:
                    self.player1.chip(self.pa2)
                    self.l_out += 1
            self.pa3 = input("start")
            if not(self.pa3 == "no"):
                self.fli = self.step0()
                self.p_sum = self.p_cul(self.cards_dc[self.fli[0]], self.cards_dc[self.fli[1]])
                self.b_sum = self.p_cul(self.cards_dc[self.fli[2]], self.cards_dc[self.fli[3]])
                print(f"プレイヤー{self.fli[0]}・{self.fli[1]}  バンカー{self.fli[2]}・{self.fli[3]}")
                print(f"プレイヤーの合計点{self.p_sum}, バンカーの合計点{self.b_sum}")
                time.sleep(1)

                self.df1 = self.df(self.p_sum, self.b_sum)
                x += 1
        self.ef1 = self.ef(self.df1[0], self.df1[1], self.pa1, self.pa2)