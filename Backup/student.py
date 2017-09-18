# encoding: utf8
import card
import random
import pickle
from player import Player
from termcolor import colored


class StudentPlayer(Player):
    wins = defeats = ties = 0
    decisions = {}
    odv = 0
    initmoney = 0
    ngames = 0
    alone = True
    new_game = True
    rules = None
    play_buffer = []
    win_streak = 0
    lose_streak = 0
    parlay = [1,2,3,4,6,9,13,19,28,41,60,88,129,189,277,406,595,872,1278,1873]  #len = 20
    fibonacci = [1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4148, 6765]   #len=20
    levels = [200,400,800,1600,3200,6400,128000]
    win_streak_number = 0
    lose_streak_number = 0
    w_more_3 = 0
    l_more_3 = 0
    level = (200,0)
    def __init__(self, name="Meu nome", money=0):
        super(StudentPlayer, self).__init__(name, money)
        self.initmoney = money
        try:
            f = open("cheats", "rb")
            self.decisions = pickle.load(f)
            f.close()
            sum = 0
            for state in self.decisions:
                if self.decisions[state].learningstate < 400:
                    sum += 1
            print('to learn: '+str(sum))
        except:
            print('Exception 1')
            pass

    def play(self, dealer, players):
        self.alone = True
        for p in players:
            if p.hand != [] and p.player.name != self.name:
                self.alone = False
                break

        ace_in_hand = soft_ace_in_hand = False
        dealer_action = None  # previous dealer action
        dealer_value = card.value(dealer.hand)
        if not self.new_game:
            dealer_action = "h" if dealer_value > self.odv else "s"

        me = ''
        my_value = 0
        for p in players:
            if p.player.name == self.name:
                me = p
                my_value = card.value(p.hand)
        sum = 0
        for c in me.hand:
            if c.is_ace():
                ace_in_hand = True
            sum += c.value()
        dealer_ace_in_hand = False
        for c in dealer.hand:
            if c.is_ace:
                dealer_ace_in_hand = True
        if sum != my_value and ace_in_hand:
            soft_ace_in_hand = True
        state = self.get_state(my_value, dealer_value, ace_in_hand, soft_ace_in_hand, dealer_action, dealer_ace_in_hand)
        try:  #
            data = self.decisions[state]
        except:
            #print('Exception 2')
            #add hand info to tmp dic
            self.decisions[state] = Info(state)
            data = self.decisions[state]

        action = data.take_action(self.new_game)
        self.new_game = False
        self.odv = dealer_value
        self.play_buffer.append((state, action))
        return action

    def want_to_play(self, rules):
        self.rules = rules
        if self.alone:
            if self.pocket >= self.initmoney * 2:
                return False
        return True

    def bet(self, dealer, players):
        #TrioPlayBetting System
        '''if self.win_streak == 0:
            self.betv = self.rules.min_bet
            if self.lose_streak > 3:
                self.betv = self.rules.min_bet
            return self.betv
        if self.win_streak == 1:
            self.betv = self.rules.min_bet + 1
            if self.betv > self.rules.max_bet:
                self.betv = self.rules.max_bet
                if self.lose_streak > 3:
                    self.betv = self.rules.min_bet
            return self.betv
        if self.win_streak == 2:
            self.betv = self.rules.min_bet + 2
            if self.betv > self.rules.max_bet:
                self.betv = self.rules.max_bet
                if self.lose_streak > 3:
                    self.betv = self.rules.min_bet
            return self.betv
        if self.win_streak == 3:
            self.betv = self.rules.min_bet + 3
            if self.betv > self.rules.max_bet:
                self.betv = self.rules.max_bet
                if self.lose_streak > 3:
                    self.betv = self.rules.min_bet
            return self.betv
        if self.win_streak == 4:
            self.betv = self.rules.min_bet + 4
            if self.betv > self.rules.max_bet:
                self.betv = self.rules.max_bet
                if self.lose_streak > 3:
                    self.betv = self.rules.min_bet
            return self.betv
        else:
            self.betv = self.rules.min_bet
            return self.betv'''
        #Fibonacci Betting System
        '''self.betv = self.fibonacci[self.win_streak]
        if self.betv < self.rules.min_bet:
            self.betv = self.rules.min_bet
        elif self.betv > self.rules.max_bet:
            self.betv = self.rules.max_bet
        return self.betv'''
        #Paroli Betting System Sequence of 3
        '''if self.win_streak == 0:
            self.betv = self.rules.min_bet
        if self.win_streak == 1:
            self.betv = self.rules.min_bet*2
            if self.betv > self.rules.max_bet:
                self.betv = self.rules.max_bet
        if self.win_streak == 2:
            self.betv = self.rules.min_bet * 4
            if self.betv > self.rules.max_bet:
                self.betv = self.rules.max_bet
                self.win_streak = 0
        return self.betv'''

        #Parlay's Betting System
        '''self.betv = self.parlay[self.win_streak]
        if self.betv < self.rules.min_bet:
            self.betv = self.rules.min_bet
        elif self.betv > self.rules.max_bet:
            self.betv = self.rules.max_bet
        return self.betv'''
        #Based on init  Betting System
        if self.pocket > self.initmoney * 2:        #200
            self.betv = self.rules.max_bet          #5
            if self.lose_streak > 2:
                self.betv = self.rules.min_bet+2
                return self.betv
        elif self.pocket > self.initmoney * 1.7:    #150
            #self.betv = self.rules.max_bet * 0.7    #4
            if self.win_streak == 0:
                self.betv = self.rules.min_bet
            if self.win_streak == 1:
                self.betv = self.rules.min_bet * 2
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
            if self.win_streak == 2:
                self.betv = self.rules.min_bet * 4
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
                    self.win_streak = 0
            return self.betv
        elif self.pocket > self.initmoney * 1.2:    #120
            #self.betv = self.rules.max_bet * 0.5    #3
            if self.win_streak == 0:
                self.betv = self.rules.min_bet
            if self.win_streak == 1:
                self.betv = self.rules.min_bet * 2
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
            if self.win_streak == 2:
                self.betv = self.rules.min_bet * 4
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
                    self.win_streak = 0
            return self.betv
        elif self.pocket > self.initmoney * 1.1:    #111
            #self.betv = self.rules.max_bet * 0.3    #2
            if self.win_streak == 0:
                self.betv = self.rules.min_bet
                if self.lose_streak > 3:
                    self.betv = self.rules.min_bet
                return self.betv
            if self.win_streak == 1:
                self.betv = self.rules.min_bet + 1
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
                    if self.lose_streak > 3:
                        self.betv = self.rules.min_bet
                return self.betv
            if self.win_streak == 2:
                self.betv = self.rules.min_bet + 2
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
                    if self.lose_streak > 3:
                        self.betv = self.rules.min_bet
                return self.betv
            if self.win_streak == 3:
                self.betv = self.rules.min_bet + 3
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
                    if self.lose_streak > 3:
                        self.betv = self.rules.min_bet
                return self.betv
            if self.win_streak == 4:
                self.betv = self.rules.min_bet + 4
                if self.betv > self.rules.max_bet:
                    self.betv = self.rules.max_bet
                    if self.lose_streak > 3:
                        self.betv = self.rules.min_bet
                return self.betv
            else:
                self.betv = self.rules.min_bet
                return self.betv
        else:
            self.betv = self.rules.min_bet
        return self.betv
        '''elif self.pocket > self.initmoney * 1.05:   #105
            self.betv = self.rules.max_bet * 0.2'''    #1


    def payback(self, prize):
        self.ngames += 1
        super(StudentPlayer, self).payback(prize)
        if self.pocket > self.level[0]:
            self.level = (self.levels[self.level[1]+1], self.level[1]+1)
        win = False
        if prize >= self.betv:  # win
            self.wins += 1
            win = True
            self.win_streak += 1
            self.lose_streak = 0
            if self.win_streak == 2:
                self.w_more_3 += 1
            self.win_streak_number += 1
            #print(self.win_streak_number)
        elif prize == 0:        # tie
            self.ties += 1
            self.win_streak += 0
        else:                   # defeat
            self.defeats += 1
            self.win_streak = 0
            self.lose_streak += 1
            if self.lose_streak == 2:
                self.l_more_3 += 1
            self.lose_streak_number += 1

        '''print(self.win_streak_number)
        print(self.w_more_3)
        print(self.lose_streak_number)
        print(self.l_more_3)'''
        for (state, action) in self.play_buffer:
            self.decisions[state].update(win, action)
        #
        self.new_game = True
        self.play_buffer = []
        if self.ngames % 5000 == 0:
            f = open("cheats", "wb")
            pickle.dump(self.decisions, f)
            f.close()

    def get_state(self, my_value, dealer_value, ace_in_hand, soft_ace_in_hand, dealer_action, dealer_ace_in_hand):
        state = ""
        state += str(my_value) + "|"
        state += str(dealer_value) + "|"
        state += "n|" if ace_in_hand == False else "y|"
        state += "n|" if soft_ace_in_hand == False else "y|"
        state += "n|" if dealer_ace_in_hand == False else "y|"
        state += "ft" if dealer_action == None else dealer_action
        return state


class Info(object):
    """Info is the class that contains all the play info for the bot to choose action"""
    hit_win = hit_lose = stand_win = stand_lose = doubledown_win = doubledown_lose = 0
    learningstate = doubledown_state = 0

    def __init__(self, state):
        super(Info, self).__init__()
        self.state = state

    def learning(self, dd=False):
        if dd:
            self.doubledown_state += 1
            return "d"
        else:
            self.learningstate += 1
            if self.learningstate < 200:
                return "s"
            elif self.learningstate >= 200 and self.learningstate < 400:
                return "h"
            else:
                try:
                    hit_profit = (self.hit_win * 1.0 / (self.hit_win + self.hit_lose))
                    stand_profit = (self.stand_win * 1.0 / (self.stand_win + self.stand_lose))
                except:
                    print('Exception 3')
                    pass

        if hit_profit >= stand_profit:
            return "h"
        else:
            return "s"

    def take_action(self, ft):
        if self.learningstate < 400:
            return self.learning()

        if ft:  # we can doubledown
            if self.doubledown_state < 40:
                return self.learning(True)
            doubledown_prob = (self.doubledown_win * 1.0 / (self.doubledown_win + self.doubledown_lose))  # dd prob
            if doubledown_prob >= 0.54:
                return "d"
        hit_profit = (self.hit_win * 1.0 / (self.hit_win + self.hit_lose))  # hit profit
        stand_profit = (self.stand_win * 1.0 / (self.stand_win + self.stand_lose))  # stand profit

        if hit_profit+stand_profit<=0.10:
            return 'u'
        mpp = max(hit_profit, stand_profit)
        if mpp == hit_profit:
            return "h"
        elif mpp == stand_profit:
            return "s"

    def update(self, win, action):
        if win:
            if action == "h":
                self.hit_win += 1
            elif action == "s":
                self.stand_win += 1
            elif action == "d":
                self.doubledown_win += 1
        else:
            if action == "h":
                self.hit_lose += 1
            elif action == "s":
                self.stand_lose += 1
            elif action == "d":
                self.doubledown_lose += 1