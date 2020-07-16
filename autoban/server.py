#!/usr/bin/python3
import asyncio
import logging
import json

from manageMessage import rocky
from lobbyLogic import lobbyManager
from autobahn.asyncio.websocket import (WebSocketServerProtocol, WebSocketServerFactory)

logging.basicConfig(level=logging.INFO)
print("Creating user object ")
rocky = rocky()
Lb=lobbyManager(rocky)


class ChatProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        try:

            #st = (request.path.split("/")[1])
            st = self.http_request_uri.split("?")[0]
            if st == "/game":
              #key = st.split("&")[0].split("=")[1]
              key=self.http_request_params['id'][0]
              room = int(self.http_request_params['Room'][0])  ## starts with zero only
              seat = int(self.http_request_params['SeatNo'][0])
              seat = seat - 1  ## for array
              room = room - 1  ## for array .
              print(key, room)
              if rocky.register(self, key, room, seat):
                  Lb.sendRoomDetails()

            elif  st == "/lobby":
                print ("Lobbbbyy")
                key=self.http_request_params['id']
                Lb.lobbyRegister(self,key)




        except Exception as ex:
            print(ex)
            print("An exception occurred, will not be registered ")

    def onOpen(self):
        try:
         st = self.http_request_uri.split("?")[0]
         if st == "/game":
             room = int(self.http_request_params['Room'][0])  ## starts with zero only
             seat = int(self.http_request_params['SeatNo'][0])
             room = room - 1
             seat = seat - 1
             if rocky.IsthereTrumpSession(self,room,seat):
                 print(" Reconect ")
             else:
                rocky.canWeStart(self,room,seat)
         elif  st == "/lobby":
            key=self.http_request_params['id']
            Lb.lobbyMessage(websocket=self)

        except Exception as ex:
             print(ex)
             print("Open  Exception  ")

    def onMessage(self, payload, is_binary):
        try:
            print(payload)
            object = json.loads(payload)
            # (rocky.listOfQ)
            ##  {"pid":pid,"card":data.value,"usr":obj.usr,"t":obj.t}  for Card Play
            ##  {"AnsNo":4,"Answer":"P","usr":"P1","t":"Team0"}'       for Villi Logic
            if 'AnsNo' in object:
                AnsNo = object['AnsNo']
                for kk in rocky.listOfQ:
                    if kk['quNo'] == AnsNo:
                        print("inside AnsNo iffff")
                        kk['status'] = 'DONE'
                        kk['ans'] = object['Answer']
                        rocky.manageVilli(AnsNo)
            elif 'pid' in object:
                pid = object['pid']
                for kk in rocky.listOfC:

                    if kk['pid'] == pid:
                        print("Card iffff")
                        kk['status'] = "DONE"
                        kk['card'] = object['card']
                        rocky.managePlay(pid)
            elif 'fid' in object:
                fid = object['fid']
                for kk in rocky.listOfF:
                    if kk['fid'] == fid:
                        print("fold in server.py")
                        kk['status'] = "DONE"
                        rocky.listOfF.remove(kk)
                        rocky.startNextMatch(kk["r"], True)

            elif 'resetID' in object:
                rocky.resetBase(object["usr"],int (object["r"])-1, int (object["SN"])-1)
            elif 'chatID' in object:
                print ("will do the chat Logic")
                Lb.chatLogic(object)

            elif   'gotoLobbyID' in object:
                rocky.gotoLobby(object["usr"],int (object["r"])-1, int (object["SN"])-1)


        except Exception as ex:
            print(ex)
            print("An exception occurred, try again ")

        # print (listOfQ)

    def onClose(self, was_clean, code, reason):
        print("closed")
        st = self.http_request_uri.split("?")[0]
        if st == "/game":
           key=self.http_request_params['id'][0]
           room = int(self.http_request_params['Room'][0])  ## starts with zero only
           seat = int(self.http_request_params['SeatNo'][0])
           room = room - 1
           rocky.unregister(self,room,seat)
           Lb.sendRoomDetails()

        elif st =="/lobby":
            Lb.lobbyUnregister(self)


        # rocky.USERS.ws.remove(self)                ## Removed from active Websockets


if __name__ == "__main__":
    print("Listening on 6789")
    factory = WebSocketServerFactory("ws://localhost:6789")
    factory.protocol = ChatProtocol

    loop = asyncio.get_event_loop()
    asyncio.Task(loop.create_server(factory, port=6789))
    loop.run_forever()
