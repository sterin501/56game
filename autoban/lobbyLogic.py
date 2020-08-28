#!/bin/python3
import asyncio
import json, random, time
from manageMessage import rocky
from parava import Parava

from autobahn.asyncio.websocket import (WebSocketServerProtocol, WebSocketServerFactory)

lobbyList = []
PV=Parava()

class lobbyManager(object):
    def __init__(self, rocky):
        self.rocky = rocky
        self.last_cleaningtime = 0

    def lobbyRegister(self, websocket, key):
        lobbyList.append(websocket)

    def lobbyMessage(self, websocket):
        print("will send lobby details ")
        # self.sendRoomDetails()
        roomAs = self.getPlayerDetails()
        payload = json.dumps({"event": "lobbyList", "roomDetails": roomAs}).encode('utf8')
        PV.mySendMessage(websocket, payload)

    def sendRoomDetails(self):
        roomAs = self.getPlayerDetails()
        payload = json.dumps({"event": "lobbyList", "roomDetails": roomAs}).encode('utf8')
        for kk in lobbyList:
            PV.mySendMessage(kk, payload)  ## kk is websocket  here



    def lobbyUnregister(self, websocket):
        lobbyList.remove(websocket)

    def getPlayerDetails(self):
        # print (self.rocky.USERS.listOfRooms)
        c = 1
        roomAs = {}
        for kk in self.rocky.USERS.listOfRooms:
            roomst = "Room" + str(c)
            playerList = []
            for player in kk:
                if player is None:
                    playerList.append("Empty")
                    continue
                playerList.append(player.userID)
            roomAs[roomst] = playerList
            c = c + 1
        return (roomAs)

    def chatLogic(self, chatObject):
        r = int(chatObject["r"]) - 1
        usr = chatObject["usr"]
        text = chatObject["text"]
        if  "role" in chatObject:
             message = {"event": "chatSend", "r": r, "usr": usr, "text": text,"role":"w"}
        else:
             message = {"event": "chatSend", "r": r, "usr": usr, "text": text}
        PV.chatSend(message,self.rocky.USERS.listOfRooms[r], self.rocky.TrumpObjects[r].watchlist)

    def pingPong(self, websocket):
        #print(websocket)
        # print (websocket.http_request_params['Room'][0])
        now = int(time.time())
        websocket.last_ping_time = now
        #print(websocket.last_ping_time)
        if (now - self.last_cleaningtime > 1800):  ## time out value  run every min , it will increase to 5 min = 300 sec
            self.last_cleaningtime = now
            print("cleaning inactive connection for smith's router")
            for kk in self.rocky.USERS.ws:
                print(kk)
                if kk.last_ping_time:
                    print(kk.last_ping_time)
                    if now - kk.last_ping_time > 125:   ## Will  match this will with js value = 60+5 = 65 second
                        print ("No ping in last 30 second "+ kk.http_request_params['id'][0] )
                        room = int(kk.http_request_params['Room'][0])  ## starts with zero only
                        seat = int(kk.http_request_params['SeatNo'][0])
                        room = room - 1
                        self.rocky.unregister(kk,room,seat)
                    else:
                        print ("Ping works fine " + kk.http_request_params['id'][0])
                else:
                    print('No last time ')
        else:
            print("@")
