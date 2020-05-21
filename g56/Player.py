#!/bin/python



class Player(object):
    def __init__(self, name,team,bot):
        self.name = name
        self.hand = []
        self.websocket=bot
        self.team=team


    def doTheDeal(self,hand):
         self.hand=hand


    def sayHello(self):
        print ("Hi! My name is {} and my Socker is  =  {}".format(self.name,self.websocket))
        return self
    # Display all the cards in the players hand
    def showHand(self):
        return (self.hand)
        #return self


    def removeCard(self,chittu):
        self.hand.remove(chittu)
