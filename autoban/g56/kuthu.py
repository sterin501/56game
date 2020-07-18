#!/bin/python
import random

order = {
    "CQ": 0, "CK": 1, "CT": 2, "CA": 3, "C9": 4, "CJ": 5,
    "HQ": 6, "HK": 7, "HT": 8, "HA": 9, "H9": 10, "HJ": 11,
    "SQ": 12, "SK": 13, "ST": 14, "SA": 15, "S9": 16, "SJ": 17,
    "DQ": 18, "DK": 19, "DT": 20, "DA": 21, "D9": 22, "DJ": 23,
}

class Card(object):
    ## C = Clubs
    ## H = Hearts
    ## S = Spades
    ## D = Diamonds

    def __init__(self):
        self.shape = ["C", "H", "S", "D"]
        # chittu=["C7","C8","C9","CT","CJ","CQ","CK","CA","H7","H8","H9","HT","HJ","HQ","HK","HA","S7","S8","S9","ST","SJ","SQ","SK","SA","D7","D8","D9","DT","DJ","DQ","DK","DA"] # 28
        deck = ["C9", "CT", "CJ", "CQ", "CK", "CA", "H9", "HT", "HJ", "HQ", "HK", "HA", "S9", "ST", "SJ", "SQ", "SK",
                "SA", "D9", "DT", "DJ", "DQ", "DK", "DA", "C9", "CT", "CJ", "CQ", "CK", "CA", "H9", "HT", "HJ", "HQ",
                "HK", "HA", "S9", "ST", "SJ", "SQ", "SK", "SA", "D9", "DT", "DJ", "DQ", "DK", "DA"]
        # order=(random.sample(xrange(0, 32),32)) # 28
        shuffledDeck = (random.sample(range(0, 48), 48))  # 56
        # print (order)
        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        p6 = []

        for kk in range(0, 8):
            p1.append(deck[shuffledDeck[kk]])
        self.p1 = sorted(p1, key=self.customSort)
        for kk in range(8, 16):
            p2.append(deck[shuffledDeck[kk]])
        self.p2 = sorted(p2, key=self.customSort)
        for kk in range(16, 24):
            p3.append(deck[shuffledDeck[kk]])
        self.p3 = sorted(p3, key=self.customSort)
        for kk in range(24, 32):
            p4.append(deck[shuffledDeck[kk]])
        self.p4 = sorted(p4, key=self.customSort)
        for kk in range(32, 40):
            p5.append(deck[shuffledDeck[kk]])
        self.p5 = sorted(p5, key=self.customSort)
        for kk in range(40, 48):
            p6.append(deck[shuffledDeck[kk]])
        self.p6 = sorted(p6, key=self.customSort)

    def customSort(self, s):
        return order[s]