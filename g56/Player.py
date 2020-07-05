#!/bin/python


class Player(object):
    def __init__(self, name, team, websocket, seatNo):
        self.name = name
        self.hand = []
        self.websocket = websocket
        self.team = team
        self.seatNo = (seatNo + 1)

    def doTheDeal(self, hand):
        self.hand = hand

    # Display all the cards in the players hand
    def showHand(self):
        return (self.hand)
        # return self

    def removeCard(self, chittu):
        self.hand.remove(chittu)
