#!/bin/python3
import random

class Gamer(object):
        def __init__(self,userID,key,websocket,room):
            self.userID=userID
            self.key=key
            self.websocket=websocket
            self.TrumpObject=""
            self.room=room
        def check(self):
            pass



class UserList(object):
    def __init__(self):
        self.UL=[]
        self.keys=[]
        self.ws=[]             ## Contins only active connection
        self.listOfRooms=[[],[],[],[],[]]  # len ([[]])  ---> 1 : 5 rooms created

    def getUserBywebSocket(self,websocket):
        for kk in self.UL:
            if kk.websocket == websocket:
               return (kk)
        return False


    def addtoList(self,gamer):
        self.UL.append(gamer)
        self.keys.append(gamer.key)
        self.ws.append(gamer.websocket)

        print ( repr(gamer) + "  is added to list")

    def removeFromRoom(self,ws):
        try:
            self.ws.remove(ws)
            print ("removef from list of ws[]")
            roomNO=-6
            for kk in self.UL:
              if (kk.websocket == ws ):
                  roomNO=kk.room
                  break
            roomObject=self.listOfRooms[roomNO]
            for kk in roomObject:
                if kk.websocket == ws:
                   roomObject.remove(kk)
                   return True
            return False
        except Exception as ex:
                    print (ex)
                    print("Error in Removing the user from room")


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

    def addGameroRomm(self,roomNO,player):
        try:
            room=self.listOfRooms[roomNO]
            room.append(player)
            return player
        except Exception as ex:
                    print (ex)
                    print ("Rooom add ")

    def canEnterTheRoom(self,user,roomNO):
            if  roomNO > 4:                         ## Max rooom ,
                print ("invalid room")
                return False
            if  len (self.listOfRooms[roomNO]) < 6:   #kk.append(user)
                return True
            else:
                print ("Room is full")
                return False


    def getRoomDetails(self,websocket):
        #room=0
        for kk in self.UL:
            if kk.websocket==websocket:
                print (kk.room)
                print (self.listOfRooms)
                return ({"room":kk.room,"gamersInRomm":self.listOfRooms[kk.room]})
        return False



    def getPlayerBywebsocket(self,websocket):
        return self.listOfRooms[room]
