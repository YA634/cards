import time
from cards_all.card import Trump_card

class Poker(): 
    dc = {"ロイヤルストレートフラッシュ":10, "ストレートフラッシュ":9, "フォーカード":8, "フルハウス":7, "フラッシュ":6, "ストレート":5, "スリーカード":4, "ツーペア":3, "ワンペア":2, "ぶた":1}

    def __init__(self, players):
        self.players_all = players
        self.card = Trump_card()
        self.players = []
        self.cards_dc = self.card.cards_dc
        self.cards_num_dc = self.card.cards_num_dc
        self.cards_sty_dc = self.card.cards_sty_dc
        self.p_li_p = []
        self.p_li_c = []
        self.op = 0
        self.pot = 0
        

    def step0_c(self):
        self.c_card_li = []
        self.c_card_li.append(self.card.drow())
        self.c_card_li.append(self.card.drow())
        self.c_card_li.append(self.card.drow())
        self.c_card_li.append(self.card.drow())
        self.c_card_li.append(self.card.drow())
        # self.c_card_li.append("♡3")
        # self.c_card_li.append("♤4")
        # self.c_card_li.append("♢5")
        # self.c_card_li.append("♧6")
        # self.c_card_li.append("♡7")
        return self.c_card_li

    def step0_p(self, m):
        self.n = 1
        self.players[self.n-1].dc = []
        while self.n <= m:
            self.players[self.n-1].drow_card_li(self.card.drow())
            self.players[self.n-1].drow_card_li(self.card.drow())
            # self.players[self.n-1].drow_card_li("")
            # self.players[self.n-1].drow_card_li("")
            print(f"プレイヤー{self.n}のドローカード {self.players[self.n-1].dc[0]}, {self.players[self.n-1].dc[1]}")
            self.n += 1

    def pa_mng(self, m, name, pa):
        if len(self.pali) == m:
            self.pali[name-1] = pa
        else:
            self.pali.append(pa)
        return self.pali
    
    def pa_print(self, m, name, cc):
        self.cmd_sel = 0
        self.command = " "
        self.b_c = "ベット(1) ";self.c_c = "コール(2) ";self.r_c = "レイズ(3) ";self.ch_c = "チェック(4) ";self.f_c = "フォールド(5)";self.ai_c = "オールイン(6)"
        if len(self.pali) == 0:
            print(f"プレイヤー{name} 強制ベット...2円")
            self.pa = "7"
            self.pc = 2
        elif len(self.pali) == 1:
            print(f"プレイヤー{name} 強制ベット...4円")
            self.pa = "7"
            self.pc = 4
        elif 1 < len(self.pali) < m:
            self.command += self.c_c + self.r_c + self.f_c
            self.cmd_sel = 1
        elif len(self.pali) == m:
            if self.turn == 0:
                self.command += self.b_c + self.ch_c + self.f_c + self.ai_c
                self.cmd_sel = 2
            else:
                self.pyc = self.point_cul(self.players[name-1].dc, cc, name)
                self.players[name-1].role = self.pyc
                self.dli = self.players[name-1].dc
                print(f"プレイヤー{name}の役は{self.pyc}です ドローカード...{self.dli}")
                if self.bc == 0:
                    self.command += self.b_c + self.ch_c + self.f_c + self.ai_c
                    self.cmd_sel = 3
                else:
                    self.command += self.c_c + self.r_c + self.f_c + self.ai_c
                    self.cmd_sel = 4
        if not(len(self.pali) == 0 or len(self.pali) == 1):
            self.pa = input(f"player{name}はベットしますか...{self.command} 所持金{self.players[name-1].money}")
            self.pa_mng(m, name, self.pa)
        else:
            self.pa_mng(m, name, self.pa)
        self.cmd_check = 0
        while self.cmd_check == 0:
            if (self.cmd_sel == 1 and (self.pa == "1" or self.pa == "4" or self.pa == "6")) or (self.cmd_sel == 2 and (self.pa == "2" or self.pa == "3")) or (self.cmd_sel == 3 and (self.pa == "2" or self.pa == "3")) or (self.cmd_sel == 4 and (self.pa == "1" or self.pa == "4")):
                print("無効なコマンドです")
                self.pa = input(f"player{name}はベットしますか...{self.command} 所持金{self.players[name-1].money}")
            elif (self.pa == "2" or self.pa == "3") and (self.players[name-1].money < self.players[name-2].chips):
                print("お金が足りません")
                self.pa = input(f"player{name}はベットしますか...{self.command} 所持金{self.players[name-1].money}")
            else:
                self.cmd_check += 1
        if self.pa == "1" or self.pa == "2" or self.pa == "3" or self.pa == "7" or self.pa == "4" or self.pa == "6":
            if self.pa == "1":
                self.pc = int(input("何円ベットしますか？ 最低ベット4円"))
                self.b_m_check = 0
                while self.b_m_check == 0:
                    if self.pc > self.players[name-1].money:
                        print("お金が足りません")
                        self.pc = int(input("何円ベットしますか？ 最低ベット4円"))
                    else:
                        self.b_m_check += 1
                self.bc += 1
            elif self.pa == "2":
                self.pc = self.players[name-2].chips
                self.bc += 1
            elif self.pa == "3":
                self.pc = self.players[name-2].chips + int(input("何円追加でレイズしますか？"))
                self.b_m_check = 0
                while self.b_m_check == 0:
                    if self.pc > self.players[name-1].money:
                        print("お金が足りません")
                        self.pc = int(input("何円ベットしますか？ 最低ベット4円"))
                    else:
                        self.b_m_check += 1
                self.bc += 1
            elif self.pa == "4":
                self.pc = 0
                print(f"player{name}はチェックしました")
            elif self.pa == "6":
                print(f"プレイヤー{name}はオールインしました")
                self.pc = self.players[name-1].money
                self.bc += 1
            self.players[name-1].chip(self.pc)
            self.pot += self.pc
        elif self.pa == "5":
            print(f"player{name}はフォールドしました")
            self.p_li_c.remove(name)
            self.players[name-1].rp_dc["role"] = "ぶた"
            self.players[name-1].rp_dc["dc_p"] = [0]
        if not(self.pa == "5"):
            print(f"player{name}のベット {self.players[name-1].chips}, 所持金残高 {self.players[name-1].money}")
        else:
            print(f"player{name}の所持金残高 {self.players[name-1].money}")

    def pa_r_ch(self, p_li):
        self.n = 0
        while len(p_li)-self.n > 0:
            self.c_m = self.players[p_li[len(p_li)-self.n-1]-1].chips-self.players[p_li[len(p_li)-self.n-2]-1].chips
            if self.c_m > 0:                
                self.players[p_li[len(p_li)-self.n-2]-1].chip(self.c_m)
                print(f"ゲーム続行のためプレイヤー{p_li[len(p_li)-self.n-2]}は{self.c_m}円を強制ベット")
                self.pot += self.c_m
            self.n += 1

    def pa_all(self, btn, m, cc):
        self.n = 1
        self.sb = (btn % m) + 1
        self.tx = 1
        for x in range(m):
            self.current_player = ((self.sb+x-1) % m) + 1
            if self.current_player in self.p_li_c:
                self.p_li = self.pa_print(m, self.current_player, cc)
        self.turn += 1
        self.bc = 0
        return self.p_li
    
    def point_cul(self, pc, cc, name):
        self.dp = [];self.dp4 = [];self.dp3 = [];self.dp2 = []
        self.ali = pc + cc
        self.n = 0
        self.num_li = []
        self.num_li2 = []
        self.sty_li = []
        self.st = 0; self.fl = 0; self.fh = 0; self.fc = 0; self.tc = 0; self.onep = 0; self.rsf = 0; self.sf = 0
        while self.n < len(self.ali):
            self.num_li2.append(self.cards_num_dc[self.ali[self.n]])
            self.n += 1
        self.n_li = sorted(self.num_li2)
        self.n_li.sort(reverse=True)
        self.h_count = 0;self.d_count = 0;self.s_count = 0;self.c_count = 0
        self.h_count = sum(1 for card in self.ali if "♡" in card)
        self.d_count = sum(1 for card in self.ali if "♢" in card)
        self.s_count = sum(1 for card in self.ali if "♤" in card)
        self.c_count = sum(1 for card in self.ali if "♧" in card)
        self.a_li = sorted(self.ali)
        if self.h_count >= 5 or self.d_count >= 5 or self.s_count >= 5 or self.c_count >= 5:
            if self.h_count >= 5:
                if len(self.a_li) == 7:
                    if not(self.h_count == 7):
                        if self.h_count == 6:
                            self.a_li.pop()
                        else:
                            self.a_li.pop(); self.a_li.pop()
                elif len(self.a_li) == 6:
                    if not(self.h_count == 6):
                        self.a_li.pop()
            elif self.d_count >= 5:
                if len(self.a_li) == 7:
                    if not(self.d_count == 7):
                        if self.d_count == 6:
                            if self.h_count == 1:
                                del self.a_li[0]
                            else:
                                self.a_li.pop()
                        else:
                            if self.h_count > 0:
                                if self.h_count == 2:
                                    del self.a_li[0];del self.a_li[0]
                                else:
                                    del self.a_li[0];self.a_li.pop()
                            else:
                                self.a_li.pop(); self.a_li.pop()
                elif len(self.a_li) == 6:
                    if not(self.d_count == 6):
                        if self.h_count == 1:
                            del self.a_li[0]
                        else:
                            self.a_li.pop()
            elif self.s_count >= 5:
                if len(self.a_li) == 7:
                    if not(self.s_count == 7):
                        if self.s_count == 6:
                            if self.h_count == 1 or self.d_count == 1:
                                del self.a_li[0]
                            else:
                                self.a_li.pop()
                        else:
                            if self.h_count > 0 or self.d_count > 0:
                                if self.h_count + self.d_count == 2:
                                    del self.a_li[0];del self.a_li[1]
                                else:
                                    del self.a_li[0];self.a_li.pop()
                            else:
                                self.a_li.pop(); self.a_li.pop()
                elif len(self.a_li) == 6:
                    if not(self.s_count == 6):
                        if self.h_count == 1 or self.d_count == 1:
                            del self.a_li[0]
                        else:
                            self.a_li.pop()
            elif self.c_count >= 5:
                if len(self.a_li) == 7:
                    if not(self.c_count == 7):
                        if self.c_count == 6:
                            del self.a_li[0]
                        else:
                            del self.a_li[0]; del self.a_li[0]
                elif len(self.a_li) == 6:
                    if not(self.c_count == 6):
                        del self.a_li[0]        
            self.n = 0
            while self.n < len(self.a_li):
                self.num_li.append(self.cards_num_dc[self.a_li[self.n]])
                self.n += 1
            self.fl += 1
            self.n_kli = sorted(self.num_li)
            self.n_jli = self.n_kli.copy()
            self.n_jli.sort(reverse=True)
            if self.n_kli[0] == 1:
                if self.n_jli[0] == 13 and self.n_jli[3] == 10:
                    self.rsf += 1
            else:
                self.st_c1 = 0
                for x in range(1,len(self.n_jli)):
                    if self.n_jli[x] == self.n_jli[x-1]-1:
                        self.st_c1 += 1
                        if self.st_c1 == 1:
                            self.dp = [self.n_jli[x]]
                    else:
                        if not(self.st_c1 >= 5):
                            self.st_c1 = 0
                if self.st_c1 >= 5:
                    self.sf += 1
            

        self.st_c2 = 0
        for x in range(1,len(self.n_li)):
            if self.n_li[x] == self.n_li[x-1]-1:
                self.st_c2 += 1
                if self.st_c2 == 1:
                    self.dp = [self.n_li[x-1]]
            else:
                if not(self.n_li[x] == self.n_li[x-1]):
                    if not(self.st_c2 >= 4):
                        self.st_c2 = 0
        if self.st_c2 >= 4:
            self.st += 1

        self.pare_c = 0
        for x in range(1,len(self.n_li)):
            if self.n_li[x] == self.n_li[x-1]:
                self.pare_c += 1
                if (x == len(self.n_li)-1):
                    if self.pare_c == 1:
                        self.onep += 1
                        self.dp2.append(self.n_li[x-1])
                    elif self.pare_c == 2:
                        self.tc += 1
                        self.dp3.append(self.n_li[x-1])
                    elif self.pare_c == 3:
                        self.fc += 1
                        self.dp4.append(self.n_li[x-1])
            else:
                if self.pare_c == 1:
                    self.onep += 1
                    self.dp2.append(self.n_li[x-1])
                elif self.pare_c == 2:
                    self.tc += 1
                    self.dp3.append(self.n_li[x-1])
                elif self.pare_c == 3:
                    self.fc += 1
                    self.dp4.append(self.n_li[x-1])
                self.pare_c = 0
        if (self.fc == 0 and self.tc == 1 and self.onep > 0):
            self.dp = [self.dp3[0],self.dp2[0]]
            self.fh += 1
        elif (self.fc == 0 and self.tc == 2):
            self.dp = [self.dp3[0],self.dp3[1]] 
            self.fh += 1
        
            

        #役計算
        if self.rsf > 0:
            self.c = "ロイヤルストレートフラッシュ"
            self.dp = []
        elif self.sf > 0:
            self.c = "ストレートフラッシュ"
        elif self.fc > 0:
            self.c = "フォーカード"
            self.dp = self.dp4
        elif self.fh > 0:
            self.c = "フルハウス"
        elif self.fl > 0:
            self.c = "フラッシュ"
            self.dp = self.n_jli
        elif self.st > 0:
            self.c = "ストレート"
        elif self.tc > 0:
            self.c = "スリーカード"
            self.dp = self.dp3
        elif self.onep > 1:
            self.c = "ツーペア"
            self.dp = self.dp2
        elif self.onep >0:
            self.c = "ワンペア"
            self.dp = self.dp2
        else:
            self.c = "ぶた"
            self.dp = self.n_li

        self.players[name-1].rp_dc["role"] = self.c
        self.players[name-1].rp_dc["dc_p"] = self.dp
        return self.c

    def ef(self, pli, p_li_all):
        if self.turn == 3:
            if len(pli) > 1:
                self.winli = self.battle(p_li_all)
                self.btl_c += 1
            self.ge += 1
        if self.ge > 0:
            self.pri_c = 0
            while self.pri_c < self.m:
                if self.pri_c+1 in pli:
                    self.role = self.players[self.pri_c].rp_dc["role"]
                    self.last_point = self.players[self.pri_c].rp_dc["dc_p"]
                    print(f"プレイヤー{self.pri_c+1}の役 {self.role}, ポイント...{self.last_point}")
                self.pri_c += 1
            if len(pli) == 1:
                print(f"winner... プレイヤー{pli[0]}, {self.pot}円獲得")
                self.players[pli[0]-1].money += self.pot
                self.pot = 0
            elif self.btl_c == 1:
                if len(self.winli) == 1:
                    print(f"winner... プレイヤー{self.winli[0]}, {self.pot}円獲得")
                    self.players[self.winli[0]-1].money += self.pot
                    self.pot = 0
                else:
                    print("引き分け") 
            else:
                print("引き分け")

    def g_all(self):
        self.bc1 = "x"; self.bc2 = "x"
        while self.turn < 3:
            self.pa_all(self.btn, self.m, self.c_card_pli)
            self.pa_r_ch(self.p_li_c)            
            time.sleep(2)
            if len(self.p_li_c) == 1:
                self.turn = 3
            if self.turn == 2:
                self.c_card_pli.append(self.c_card[3])
                self.bc1 = self.c_card[3]
            elif self.turn == 3:
                self.c_card_pli.append(self.c_card[4])
                self.bc1 = self.c_card[3]
                self.bc2 = self.c_card[4]
            print(f"コミュニティカード... {self.c_card[0]}, {self.c_card[1]}, {self.c_card[2]}, {self.bc1}, {self.bc2}")
            self.last_pc_c = 0
            while self.last_pc_c < len(self.p_li_c):
                self.point_cul(self.players[self.p_li_c[self.last_pc_c]-1].dc, self.c_card_pli, self.p_li_c[self.last_pc_c])
                self.last_pc_c += 1
            self.ef(self.p_li_c, self.p_li_p)

    def battle(self, p_li_all):
        self.pt_li = []
        self.winner = []
        self.m_pt_li = []
        for x in range(len(p_li_all)):
            self.pt_li.append(self.dc[self.players[x].rp_dc["role"]])
        for x in range(len(p_li_all)):
            if self.pt_li[x] == max(self.pt_li):
                self.winner.append(x+1)
        if len(self.winner) > 1:
            for x in range(len(p_li_all)):
                if x+1 in self.winner:
                    self.dc_p_li = self.players[x].rp_dc["dc_p"]
                    if len(self.dc_p_li) > 0:
                        if 1 in self.dc_p_li:
                            self.m_pt_li.append(14)
                        else:
                            self.m_pt_li.append(self.dc_p_li[0])
                    else:
                        self.m_pt_li.append(0)
                else:
                    self.m_pt_li.append(0)
            self.winner = []
            for x in range(len(self.m_pt_li)):
                if self.m_pt_li[x] == max(self.m_pt_li):
                    self.winner.append(x+1)
        return self.winner



    # def start(self):
    #     self.m = int(input("何人で始めますか(2〜10人)"))
    #     if not(self.m in [2, 3, 4, 5, 6, 7, 8, 9, 10]):
    #         self.m = int(input("何人で始めますか(1〜5人)"))        
    #     print(f"{self.m}人で{self.m}回のゲームを行います...")
    #     self.mc = 1
    #     while self.mc <= self.m:
    #         self.players.append(self.players_all[self.mc-1])
    #         self.p_li_p.append(self.mc)
    #         self.mc += 1
    #     self.btn = 1
    #     while self.btn <= self.m:
    #         self.ge = 0 ;self.turn = 0 ;self.bc = 0;self.btl_c = 0;self.pali = []
    #         self.p_li_c = self.p_li_p.copy()
    #         print(f"btnは...player{self.btn}です")
    #         self.step0_p(self.m)
    #         self.c_card = []
    #         self.c_card = self.step0_c()
    #         self.c_card_pli = [self.c_card[0], self.c_card[1], self.c_card[2]]
    #         self.g_all()
    #         self.btn += 1            
    #         time.sleep(1)
    #         if self.btn < self.m:
    #             print("次のゲームを始めます")
    #         self.turn = 0
    #         time.sleep(2)
