#!/bin/python3
from g56.Player import Player
from g56.RuleBook import Points
from g56.kuthu import Card
from g56.table import Table


class TrumpHandler(object):
    def __init__(self, RoomIsFull):
        self.P1 = Player(RoomIsFull[0].userID, "Team0", RoomIsFull[0].websocket, RoomIsFull[0].seatNo)
        self.P2 = Player(RoomIsFull[1].userID, "Team1", RoomIsFull[1].websocket, RoomIsFull[1].seatNo)
        self.P3 = Player(RoomIsFull[2].userID, "Team0", RoomIsFull[2].websocket, RoomIsFull[2].seatNo)
        self.P4 = Player(RoomIsFull[3].userID, "Team1", RoomIsFull[3].websocket, RoomIsFull[3].seatNo)
        self.P5 = Player(RoomIsFull[4].userID, "Team0", RoomIsFull[4].websocket, RoomIsFull[4].seatNo)
        self.P6 = Player(RoomIsFull[5].userID, "Team1", RoomIsFull[5].websocket, RoomIsFull[5].seatNo)
        self.tt = Table(self.P1, self.P2, self.P3, self.P4, self.P5, self.P6) ## g%6 table reference
        self.rules = Points()  ## Might need to chagne every game
        self.thisPlay = []
        self.thisPlayForSunu = []  ## This is for javascript logic
        print("Starting Table in Califorina")  ## Will replaced by Room 1
        self.ShuffledCards=""
        self.spinner=1
        self.watchlist=[]

    def publicTextBeforeEveryMatch(self):
        # while True:

        st = ""
        st = st + ("Game " + str(self.tt.gameCount))
        st = st + ("Frist player is  " + self.tt.orderofPlay[0].name)
        return st

    def doTheDeal(self):
        self.rules = Points() ## WIll reset all points
        self.ShuffledCards = Card()
        self.P1.hand = self.ShuffledCards.p1
        self.P2.hand = self.ShuffledCards.p2
        self.P3.hand = self.ShuffledCards.p3
        self.P4.hand = self.ShuffledCards.p4
        self.P5.hand = self.ShuffledCards.p5
        self.P6.hand = self.ShuffledCards.p6


    def getOrderInPlayer(self,player):
        c=0
        for kk in self.tt.orderofPlay:
            if kk == player:
                return c
            c=c+1
        return ("Issue")

    def getPlayerBySeat(self,userID,websocket,seatNo):
        team = 'Team0' if seatNo%2==0 else 'Team1'
        if seatNo == 0 and self.P1 is None:
            self.P1 = Player(userID, team, websocket,seatNo)
            self.P1.hand = self.ShuffledCards.p1
            orderofPlayIndex=self.getOrderInPlayer(self.tt.P1)
            self.tt.P1=self.P1
            self.tt.orderofPlay[orderofPlayIndex]=self.P1
            return self.P1
        elif seatNo == 1 and self.P2 is None:
            self.P2 = Player(userID, team, websocket,seatNo)
            self.P2.hand = self.ShuffledCards.p2
            orderofPlayIndex=self.getOrderInPlayer(self.tt.P2)
            self.tt.P2=self.P2
            self.tt.orderofPlay[orderofPlayIndex]=self.P2
            return self.P2
        elif seatNo == 2 and self.P3 is None:
            self.P3 = Player(userID, team, websocket,seatNo)
            self.P3.hand = self.ShuffledCards.p3
            orderofPlayIndex=self.getOrderInPlayer(self.tt.P3)
            self.tt.P3=self.P3
            self.tt.orderofPlay[orderofPlayIndex]=self.P3
            return self.P3
        elif seatNo == 3 and self.P4 is None:
            self.P4 = Player(userID, team, websocket,seatNo)
            self.P4.hand = self.ShuffledCards.p4
            orderofPlayIndex=self.getOrderInPlayer(self.tt.P4)
            self.tt.P4=self.P4
            self.tt.orderofPlay[orderofPlayIndex]=self.P4
            return self.P4
        elif seatNo == 4 and self.P5 is None:
            self.P5 = Player(userID, team, websocket,seatNo)
            self.P5.hand = self.ShuffledCards.p5
            orderofPlayIndex=self.getOrderInPlayer(self.tt.P5)
            self.tt.P5=self.P5
            self.tt.orderofPlay[orderofPlayIndex]=self.P5
            return self.P5
        elif seatNo == 5 and self.P6 is None:
            self.P6 = Player(userID, team, websocket,seatNo)
            self.P6.hand = self.ShuffledCards.p6
            orderofPlayIndex=self.getOrderInPlayer(self.tt.P6)
            self.tt.P6=self.P6
            self.tt.orderofPlay[orderofPlayIndex]=self.P6
            return self.P6
        else:
            print ("No vacant seat ")
            return ("Not vacant")
