import random
class Trump_card:
    # li1 = ["♡", "♤", "♧", "♢"]
    li1 = ["heart_", "spade_", "club_", "diamond_"]
    li2 = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
    li3 = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    li4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    def __init__(self):
        self.cards_dc = {}
        self.cards_li = []
        self.create()
    
    def create(self):
        self.cards_dc = {self.li1[i]+self.li2[j]: self.li3[j] for i in range(4) for j in range(13)}
        self.cards_li = [self.li1[i]+self.li2[j] for i in range(4) for j in range(13)]
        self.cards_num_dc = {self.li1[i]+self.li2[j]: self.li4[j] for i in range(4) for j in range(13)}
        self.cards_sty_dc = {self.li1[i]+self.li2[j]: self.li1[i] for i in range(4) for j in range(13)}
        self.cards_mdc = {self.li1[i]+self.li2[j]: self.li2[j] for i in range(4) for j in range(13)}

    def drow(self):
        if len(self.cards_li) > 0:
            self.drow_card = random.choice(self.cards_li)
            self.cards_li.remove(self.drow_card)
            return self.drow_card
        else:
            self.drow_card = "None"
            return self.drow_card
    
    # def show(self, x):
    #     self.sty = self.cards_sty_dc[x]
    #     self.num = self.cards_num_dc[x]
    #     if self.num == 11:
    #         self.cn = f"{self.sty}jack"
    #     elif self.num == 12:
    #         self.cn = f"{self.sty}queen"
    #     elif self.num == 13:
    #         self.cn = f"{self.sty}king"
    #     else:
    #         self.cn = f"{self.sty}{self.num}"
    #     return f"{self.cn}.png"

                        