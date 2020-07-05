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
        self.tt = Table(self.P1, self.P2, self.P3, self.P4, self.P5, self.P6)
        self.rules = Points()  ## Might need to chagne every game
        self.thisPlay = []
        self.thisPlayForSunu = []  ## This is for javascript logic
        print("Starting Table in Califorina")  ## Will replaced by Room 1

    def publicTextBeforeEveryMatch(self):
        # while True:

        st = ""
        st = st + ("Game " + str(self.tt.gameCount))
        st = st + (" Lets start maggie")
        st = st + ("Make the deal______________________________________")
        st = st + ("Frist player (Kallikaran )  is  " + self.tt.orderofPlay[0].name)
        return st

    # self.doTheDeal()
    # self.setThurpu()   ## Might need to chagne

    def doTheDeal(self):
        self.rules = Points()
        ss = Card()
        self.P1.hand = ss.p1
        self.P2.hand = ss.p2
        self.P3.hand = ss.p3
        self.P4.hand = ss.p4
        self.P5.hand = ss.p5
        self.P6.hand = ss.p6
