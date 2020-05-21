#!/bin/python3
import random

class Gamer(object):
        def __init__(self,userID,key,websocket):
            self.userID=userID
            self.key=key
            self.websocket=websocket
            self.TrumpObject=""
        def check(self):
            pass



class UserList(object):
    def __init__(self):
        self.UL=[]
        self.keys=[]
        self.ws=[]


    def addtoList(self,gamer):
        self.UL.append(gamer)
        self.keys.append(gamer.key)
        self.ws.append(gamer.websocket)

        print ( repr(gamer) + "  is added to list")

    def removFromList(self,gamer):

        #self.UL.remove(gamer)
        try :
           #self.ws.remove(gamer.websocket)
           print ("Will remove it later")
        except Exception as ex:
             print ("not in the list")

    def getKeyBySocket(self,ws):
        for kk in self.UL:
            if kk.websocket == ws:
                return (kk.key)
        return False

    def checkForkey(self,key):  ## will replace with sqllite
        #print (key +"  checking ")
        if key in self.keys:
            print (" in if")
            print (self.UL)
            for kk in self.UL:
                print (kk)
                if kk.key == key:
                  return (kk)
        else:
            return False

    def creatBotPlayers(self):
        for i in range(0,3):
            gg=Gamer(("A")+ str( random.randint(9,7568)),str( random.randint(9,7568)),False)
            self.UL.append(gg)
        print (self.UL)   
