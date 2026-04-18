from cards_all.card import Trump_card
import random
from accounts.utils import update_user_money, can_bet
# from player import Player
import time

class Blackjack():   
    def __init__(self, cards_li):
        self.card = Trump_card()
        self.players = []
        self.cards_dc = self.card.cards_dc
        if len(cards_li) == 0:
            self.cards_li = self.card.cards_li
        else:
            self.cards_li = cards_li
        self.cards_mdc = self.card.cards_mdc
        self.dc = []
        self.acs = ['ヒット','スタンド']
        self.process_end = 0
        # self.players_all = players
        self.sp1_li = []
        self.sp2_li = []

    def step0_d(self):
        self.n = 0
        self.ddli = []
        self.ddli.append(self.card.drow())
        self.ddli.append(self.card.drow())
        return self.ddli

    def step0_p(self, m):
        self.n = 1
        while self.n <= m:
            self.dc1 = self.card.drow()
            self.dc2 = self.card.drow()
            self.players[self.n-1].drow_card_li(self.dc1)
            self.players[self.n-1].drow_card_li(self.dc2)
            self.pcl = [self.dc1, self.dc2]
            self.pp = self.pc(self.players[self.n-1].dc)
            print(f"プレイヤー{self.n}のドローカード {self.dc1}, {self.dc2}, {self.pp}ポイント")
            if self.pp == 21:
                self.bj += 1
            self.n += 1
        return self.pcl

    def drow(self):
        if len(self.cards_li) > 0:
            self.drow_card = random.choice(self.cards_li)
            self.cards_li.remove(self.drow_card)
            return self.drow_card
        else:
            self.drow_card = "None"
            return self.drow_card

    def pc(self, li):
        self.sum = 0
        self.o = 0
        while self.o < len(li):
            self.sum += self.cards_dc[li[self.o]]
            self.o += 1
        ace_count = sum(1 for card in li if 'ace' in card)
        while self.sum > 21 and ace_count > 0:
            self.sum -= 10
            ace_count -= 1
        return self.sum
    
    def ex_drow(self, name):
        self.ex_dc = self.card.drow()
        self.players[name].drow_card_li(self.ex_dc)
        return self.ex_dc

    def ex_ac(self,dli,pli):
        self.pli = pli
        if self.cards_dc[dli[0]] == 11:
            if self.pc(self.pli) == 21 and len(self.pli) == 2:
                self.ex_acs = ['イーブンマネー','no']
            else:
                if self.cards_mdc[self.pli[0]] == self.cards_mdc[self.pli[1]]:
                    self.ex_acs = ['ダブルダウン','インシュアランス','スプリッティングペアー','サレンダー','no']
                else:
                    self.ex_acs = ['ダブルダウン','インシュアランス','サレンダー','no']                   
        else:
            if self.pc(self.pli) == 21 and len(self.pli) == 2:
                self.ex_acs = ['no']
            else:
                if self.cards_mdc[self.pli[0]] == self.cards_mdc[self.pli[1]]:
                    self.ex_acs = ['ダブルダウン','スプリッティングペアー','サレンダー','no']
                else:
                    self.ex_acs = ['ダブルダウン','サレンダー','no']
        return self.ex_acs

    def ex_faze(self, dli, pli, m, ex_ac):
        # self.n = 1       
        # while self.n <= m:
        self.message = ""
        # self.pli = self.players[self.n-1].dc
        self.pli = pli
        # if self.players[self.n-1].ex_action == 0:
        #     if self.cards_dc[dli[0]] == 11:
        #         if self.pc(self.pli) == 21 and len(self.pli) == 2:
        #             self.ex_ac = input(f"プレイヤー{self.n}は特殊アクションを行いますか？ イーブンマネー(5) or no(3)")
        #         else:
        #             if self.cards_mdc[self.pli[0]] == self.cards_mdc[self.pli[1]]:
        #                 self.ex_ac = input(f"プレイヤー{self.n}は特殊アクションを行いますか？ ダブルダウン(1) or インシュアランス(4) or スプリッティングペアー(6) or サレンダー(2) or no(3)")
        #             else:
        #                 self.ex_ac = input(f"プレイヤー{self.n}は特殊アクションを行いますか？ ダブルダウン(1) or インシュアランス(4) or サレンダー(2) or no(3)")                    
        #     else:
        #         if self.pc(self.pli) == 21 and len(self.pli) == 2:
        #             self.ex_ac = input(f"プレイヤー{self.n}は特殊アクションを行いますか？ no(3)")
        #         else:
        #             if self.cards_mdc[self.pli[0]] == self.cards_mdc[self.pli[1]]:
        #                 self.ex_ac = input(f"プレイヤー{self.n}は特殊アクションを行いますか？ ダブルダウン(1) or スプリッティングペアー(6) サレンダー(2) or no(3)")
        #             else:
        #                 self.ex_ac = input(f"プレイヤー{self.n}は特殊アクションを行いますか？ ダブルダウン(1) or サレンダー(2) or no(3)")
        #     self.players[self.n-1].ex_action += 1
        # else:
        #     self.ex_ac == "3"
        self.ex_act = ex_ac
        print(self.ex_act)
        if self.ex_act == "ダブルダウン":
            print(f"プレイヤー{self.n}はダブルダウンを選択しました")
            self.players[self.n-1].dd += 1
            self.ed = self.ex_drow(self.n-1)
            self.pp = self.pc(self.pli)
            print(f"プレイヤー{self.n}のドローカード {self.ed}, {self.pp}ポイント")
            if self.pp >= 21:
                if self.pp > 21:
                    print("あなたはバーストしました")
                    self.bst += 1
                else:
                    print("あなたは21ポイントになりました")
            self.n += 1
        elif self.ex_act == "サレンダー":
            self.players[self.n-1].ef += 1
            print(f"プレイヤー{self.n}はサレンダーを選択しました")
            print(f"{self.players[self.n-1].chips//2}円lost")
            self.n += 1
        elif self.ex_act == "イーブンマネー":
            self.players[self.n-1].ef += 1
            print(f"プレイヤー{self.n}はイーブンマネーを選択しました")
            print(f"{self.players[self.n-1].chips*2}円get")
            self.n += 1
        elif self.ex_act == "スプリッティングペアー":
            print('access_success')
            self.process_end += 1
            if self.process_end == 1:
                self.message = "スプリッティングペアーを選択しました"
            self.new_pli = [self.pli[0],self.drow()]
            self.message += f'{self.process_end}番目の手札'
            return {'ex_ac':ex_ac,'process_end':self.process_end,'pli':self.new_pli,'message':self.message}
        elif self.ex_act == "no" or self.ex_act == "インシュアランス":
            # if self.ex_act == "インシュアランス":
            #     print(f"プレイヤー{self.n}はインシュアランスを選択しました")
            #     print(f"{self.players[self.n-1].chips//2}円を保険として賭けます...")
            #     print("open")
            #     self.dp = self.pc(dli)
            #     print(f"ディーラーのハンド {dli[0]}, {dli[1]}")
            #     if self.cards_dc[dli[1]] == 10:
            #         print("blackjack!!")
            #         print(f"プレイヤー{self.n}は{self.players[self.n-1].chips}円lost、{self.players[self.n-1].chips}円get")
            #         self.players[self.n-1].ef += 1
            #         self.n += 1
            #         break
            #     else:
            #         print("インシュランス失敗")
            # self.ex_pa = input(f"プレイヤー{self.n}は追加のドローを行いますか？ yes(1) or no(2)")
            # if self.ex_pa == "yes" or self.ex_pa == "1":
            #     self.ed = self.ex_drow(self.n-1)
            #     self.pp = self.pc(self.pli)
            #     print(f"プレイヤー{self.n}のドローカード {self.ed}, {self.pp}ポイント")
            #     if self.pp >= 21:
            #         if self.pp > 21:
            #             print("あなたはバーストしました")
            #             self.bst += 1
            #         else:
            #             print("あなたは21ポイントになりました")
            #         self.n += 1
            # elif self.ex_pa == "no" or self.ex_pa == "2":
            #     self.n += 1
            self.process_end = 100
            self.message = 'noを選択しました'
            return {'ex_ac':ex_ac,'process_end':self.process_end,'pli':pli,'message':self.message}

    def normal_faze(self, ac):
        if ac == 'ヒット':
            self.ex_dr = self.drow()
            return self.drow()
        else:
            return None
        

    def lc(self, username, pli, pm, dp):
        self.x = 0
        if self.x == 1:
        # if not(self.players[self.n-1].sp == 0):
            self.lsp_num = 1
            # while self.lsp_num <= 2:
            #     self.spli = self.players[self.n-1].drow_card_li_sp("♡10", self.lsp_num)
            #     self.spli.remove("♡10")
            #     # self.pp = self.pc(self.players[self.n-1].drow_card_li_sp(0, self.lsp_num))
            #     self.pp = self.pc(self.spli)
            #     if 21 >= self.pp > dp or dp > 21 >= self.pp:
            #         if self.pp == 21 and len(self.spli) == 2:
            #             print("blackjack!!")
            #             self.players[self.n-1].money += pm*3/2
            #             print(f"プレイヤー{pn}_{self.lsp_num} {pm*5/2}円get 残高{self.players[self.n-1].money}")
            #         else:
            #             print(f"プレイヤー{pn}_{self.lsp_num} あなたの勝ち")
            #             self.players[self.n-1].money += pm
            #             print(f"{pm*2}円get 残高{self.players[self.n-1].money}")
            #     elif 21 >= dp > self.pp:
            #         print(f"プレイヤー{pn}_{self.lsp_num} あなたの負け")
            #         self.players[self.n-1].money -= pm
            #         print(f"{pm}円lost 残高{self.players[self.n-1].money}")
            #     elif self.pp > 21:
            #         print(f"プレイヤー{pn}_{self.lsp_num} あなたの負け")
            #         self.players[self.n-1].money -= pm
            #         print(f"{pm}円lost 残高{self.players[self.n-1].money}")
            #     else:
            #         print(f"プレイヤー{pn}_{self.lsp_num} 同点")
            #         print(f"{pm}円back 残高{self.players[self.n-1].money}")
            #     self.lsp_num += 1
        else:
            self.pp = self.pc(pli)
            # if self.players[pn-1].dd == 0: ダブルダウン
            if self.x == 0:
                if 21 >= self.pp > dp or dp > 21 >= self.pp:
                    if self.pp == 21 and len(pli) == 2:
                        # print("blackjack!!")
                        self.amount = pm*3/2
                        # self.players[self.n-1].money += pm*3/2
                        self.result = f'ブラックジャック！ あなたの勝ち {self.amount}円get'
                        # print(f"プレイヤー{pn} {pm*5/2}円get 残高{self.players[self.n-1].money}")
                    else:
                        # print(f"プレイヤー{pn} あなたの勝ち")
                        self.amount = pm
                        # self.players[self.n-1].money += pm
                        self.result = f'あなたの勝ち {self.amount}円get'
                        # print(f"{pm*2}円get 残高{self.players[self.n-1].money}")
                elif 21 >= dp > self.pp:
                    # print(f"プレイヤー{pn} あなたの負け")
                    # self.players[self.n-1].money -= pm
                    self.amount = 0
                    self.result = f'あなたの負け {self.amount}円get'
                    # print(f"{pm}円lost 残高{self.players[self.n-1].money}")
                elif self.pp > 21:
                    # print(f"プレイヤー{pn} あなたの負け")
                    # self.players[self.n-1].money -= pm
                    # print(f"{pm}円lost 残高{self.players[self.n-1].money}")
                    self.amount = 0
                    self.result = f'あなたの負け {self.amount}円get'
                else:
                    # print(f"プレイヤー{pn} 同点")
                    # print(f"{pm}円back 残高{self.players[self.n-1].money}")
                    self.amount = pm
                    self.result = f'引き分け {self.amount}円get'
            else:
                self.amount = 0
                # if 21 >= self.pp > dp or dp > 21 >= self.pp:
                #     if self.pp == 21 and len(pli) == 2:
                #         print("blackjack!!")
                #         self.players[self.n-1].money += pm*3/2
                #         print(f"プレイヤー{pn} {2*pm*5/2}円get 残高{self.players[self.n-1].money}")
                #     else:
                #         print(f"プレイヤー{pn} あなたの勝ち")
                #         self.players[self.n-1].money += pm
                #         print(f"{2*pm*2}円get 残高{self.players[self.n-1].money}")
                # elif 21 >= dp > self.pp:
                #     print(f"プレイヤー{pn} あなたの負け")
                #     self.players[self.n-1].money -= pm
                #     print(f"{2*pm}円lost 残高{self.players[self.n-1].money}")
                # elif self.pp > 21:
                #     print(f"プレイヤー{pn} あなたの負け")
                #     self.players[self.n-1].money -= pm
                #     print(f"{2*pm}円lost 残高{self.players[self.n-1].money}")
                # else:
                #     print(f"プレイヤー{pn} 同点")
                #     print(f"{2*pm}円back 残高{self.players[self.n-1].money}")
        
        return {'result':self.result}


    def d_ef(self, dli, pli):
        self.result = "open  "
        self.dp = self.pc(dli)
        self.ex_d_card = []
        self.result += f"ディーラーのハンド {dli[0]}, {dli[1]}, {self.dp}ポイント  "
        self.pp = self.pc(pli)
        if self.pp <= 21:
            while self.dp < 17:
                self.d_ed = self.drow()
                self.result += f"追加ドロー...{self.d_ed}"
                self.ex_d_card.append(self.d_ed)
                dli.append(self.d_ed)
                self.dp = self.pc(dli)
        self.result += f"ディーラーの最終ポイント {self.dp}ポイント"
        return {'result':self.result,'dp':self.dp,'pp':self.pp,'ex_d_card':self.ex_d_card}
        # self.n = 1 
        # time.sleep(2)
        # while self.n <= m:
        #     if self.players[self.n-1].ef == 0:
        #             self.lc(self.n, self.players[self.n-1].dc, self.players[self.n-1].chips, self.dp)
        #         # else:
        #         #     self.lc(f"{self.n}_1", self.players[self.n-1].dc_1, self.players[self.n-1].chips, self.dp)
        #         #     self.lc(f"{self.n}_2", self.players[self.n-1].dc_2, self.players[self.n-1].chips, self.dp)
        #     self.n += 1

    def start(self):
        self.m = int(input("何人で始めますか(1〜5人)"))
        if not(self.m in [1, 2, 3, 4, 5]):
            self.m = int(input("何人で始めますか(1〜5人)"))        
        self.bst = 0;self.bj = 0;self.cc = 1
        # while self.cc <= self.m:
        #     self.players.append(self.players_all[self.cc-1])
        #     self.cp = int(input(f"プレイヤー{self.cc}の賭け金を入力してください 残り残高{self.players[self.cc-1].money}"))
        #     # self.players[self.cc-1].chip(self.cp)
        #     self.players[self.cc-1].chips = int(self.cp)
        #     self.cc += 1
        self.ff = self.step0_d()
        # self.ff = ["♡ace", "♡10"]
        print(f"ディーラーのドローカード {self.ff[0]}, x")
        self.dp = self.pc(self.ff)
        self.pl = self.step0_p(self.m)
        # self.players[0].dc = ["♡ace","♤ace"];self.bj = 0             #デバック用
        # print(f"プレイヤー{1}のドローカード {self.players[0].dc[0]}, {self.players[0].dc[1]}, ~ポイント")
        if self.bj == self.m and not(self.cards_dc[self.ff[0]] == 11):
            self.n = 1
            while self.n <= self.m:
                self.lc(self.n, self.players[self.n-1].dc, self.players[self.n-1].chips, self.dp)
                self.n += 1
        else:
            self.ex_faze(self.ff, self.m)
            time.sleep(1)
            if self.bst == self.m:
                self.n = 1
                while self.n <= self.m:
                    self.lc(self.n, self.players[self.n-1].dc, self.players[self.n-1].chips, self.dp)
                    self.n += 1
            else:
                self.d_ef(self.ff, self.m)

