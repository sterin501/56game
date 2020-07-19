#!/bin/python3
import random



class Card(object):
    ## C = Clubs
    ## H = Hearts
    ## S = Spades
    ## D = Diamonds

    def __init__(self):
        self.order = {               ## for custom sort with value of card
            "CQ": 0, "CK": 1, "CT": 2, "CA": 3, "C9": 4, "CJ": 5,
            "HQ": 6, "HK": 7, "HT": 8, "HA": 9, "H9": 10, "HJ": 11,
            "SQ": 12, "SK": 13, "ST": 14, "SA": 15, "S9": 16, "SJ": 17,
            "DQ": 18, "DK": 19, "DT": 20, "DA": 21, "D9": 22, "DJ": 23,
        }

        deck = ["C9", "CT", "CJ", "CQ", "CK", "CA", "H9", "HT", "HJ", "HQ", "HK", "HA", "S9", "ST", "SJ", "SQ", "SK",
                "SA", "D9", "DT", "DJ", "DQ", "DK", "DA", "C9", "CT", "CJ", "CQ", "CK", "CA", "H9", "HT", "HJ", "HQ",
                "HK", "HA", "S9", "ST", "SJ", "SQ", "SK", "SA", "D9", "DT", "DJ", "DQ", "DK", "DA"]
        # order=(random.sample(xrange(0, 32),32)) # 28
        #shuffledDeck = (random.sample(range(0, 48), 48))  # 56
        random.shuffle(deck) ## THis will do shuffle by random class .
        p1=deck[0:8]
        self.p1 = sorted(p1, key=self.customSort)
        p2=deck[8:16]
        self.p2 = sorted(p2, key=self.customSort)
        p3=deck[16:24]
        self.p3 = sorted(p3, key=self.customSort)
        p4=deck[24:32]
        self.p4 = sorted(p4, key=self.customSort)
        p5=deck[32:40]
        self.p5 = sorted(p5, key=self.customSort)
        p6=deck[40:48]
        self.p6 = sorted(p6, key=self.customSort)

    def customSort(self, s):  ## Added by Urmi for Mannan's way for sorting for card value , Rather than English sort
        return self.order[s]
