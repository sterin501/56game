#!/bin/python3
import random



class Card(object):
    ## C = Clubs
    ## H = Hearts
    ## S = Spades
    ## D = Diamonds
    ## T is 10 . 9 is  , K is King etc

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
        #while True:
        #     ## THis will do shuffle by random class .
        #    if self.condidtionCheck(deck):
        #        break
        random.shuffle(deck)
        p1=deck[0:4]+deck[24:28]   ## Ganesh need this way to shuffle the card . Like offline play
        self.p1 = sorted(p1, key=lambda x: self.order[x], reverse=True)  ## Added by smith to custom sort by lambda method to look cool
        p2=deck[4:8]+deck[28:32]
        self.p2 = sorted(p2, key=lambda x: self.order[x], reverse=True)
        p3=deck[8:12]+deck[32:36]
        self.p3 = sorted(p3, key=lambda x: self.order[x], reverse=True)
        p4=deck[12:16]+deck[36:40]
        self.p4 = sorted(p4, key=lambda x: self.order[x], reverse=True)
        p5=deck[16:20]+deck[40:44]
        self.p5 = sorted(p5, key=lambda x: self.order[x], reverse=True)
        p6=deck[20:24]+deck[44:48]
        self.p6 = sorted(p6, key=lambda x: self.order[x], reverse=True)

        # p1=deck[0:8]
        # self.p1 = sorted(p1, key=lambda x: self.order[x], reverse=True)  ## Added by smith to custom sort by lambda method to look cool
        # p2=deck[8:16]
        # self.p2 = sorted(p2, key=lambda x: self.order[x], reverse=True)
        # p3=deck[16:24]
        # self.p3 = sorted(p3, key=lambda x: self.order[x], reverse=True)
        # p4=deck[24:32]
        # self.p4 = sorted(p4, key=lambda x: self.order[x], reverse=True)
        # p5=deck[32:40]
        # self.p5 = sorted(p5, key=lambda x: self.order[x], reverse=True)
        # p6=deck[40:48]
        # self.p6 = sorted(p6, key=lambda x: self.order[x], reverse=True)
    def condidtionCheck(self,cards):  ## Not using now .. Serial 56er Poona has not called 56 after that 
       p1=cards[0:4]+cards[24:28]
       p2=cards[4:8]+cards[28:32]
       p3=cards[8:12]+cards[32:36]
       p4=cards[12:16]+cards[36:40]
       p5=cards[16:20]+cards[40:44]
       p6=cards[20:24]+cards[44:48]
       ## condition1 , at lease one point to player
       for kk in [p1,p2,p3,p4,p5,p6]:
           point=False
           for ss in kk:
               if ss[1] in ["9","T","J","A"]:
                   point=True
                   break
           if not  point:
               print ( " Condition 1 failed , need to suffule again ")
               return False
       ## condtion2 , at least one sign in any player in the team
       team1=p1+p3+p5
       team2=p2+p4+p6
       signs = set ([item[0] for item in team1] )
       if  len (signs) !=4:
           print ( " Condition 2 failed , need to suffule again ")
           return False
       signs = set ([item[0] for item in team2] )
       if  len (signs) !=4:
           print ( " Condition 2 failed , need to suffule again ")
           return False
       return True
