#!/bin/python3
import asyncio
import json,random
from manageMessage import rocky

from autobahn.asyncio.websocket import (WebSocketServerProtocol,WebSocketServerFactory)



lobbyList=[]


class lobbyManager(object):
    def __init__(self,rocky):
        self.rocky=rocky


    def lobbyRegister(self,websocket,key):
        lobbyList.append (websocket)

    def lobbyMessage(self,websocket):
       print ("will send lobby details ")
       #self.sendRoomDetails()
       roomAs=self.getPlayerDetails()
       payload = json.dumps({"event": "lobbyList", "roomDetails": roomAs}).encode('utf8')
       self.mySendMessage(websocket,payload)




    def  sendRoomDetails(self):
         roomAs=self.getPlayerDetails()
         payload = json.dumps({"event": "lobbyList", "roomDetails": roomAs}).encode('utf8')
         for kk in lobbyList:
             self.mySendMessage(kk,payload)  ## kk is websocket  here


    def mySendMessage(self, websocket, payload):
            try:
                websocket.sendMessage(payload, False)
                return True
            except Exception as ex:
                print(ex)
                print("CODE:2019 Can't sendMessage to client from lobby")
            return False

    def lobbyUnregister(self,websocket):
        lobbyList.remove(websocket)

    def getPlayerDetails(self):
        #print (self.rocky.USERS.listOfRooms)
        c=1
        roomAs={}
        for kk in self.rocky.USERS.listOfRooms:
            roomst="Room"+ str(c)
            playerList=[]
            for player in kk:
                if player is None:
                    playerList.append("Empty")
                    continue
                playerList.append(player.userID)
            roomAs[roomst]=playerList
            c=c+1
        return (roomAs)
