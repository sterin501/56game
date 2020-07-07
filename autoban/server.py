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
            print (st)
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
        #print(self.http_headers)
        #print (self.http_request_uri)
        #print (self.http_request_params)
        st = self.http_request_uri.split("?")[0]
        print (st)
        if st == "/game":
          if rocky.IsthereTrumpSession(websocket=self):
            print(" Reconect ")
          else:
            rocky.canWeStart(websocket=self)
        elif  st == "/lobby":
            key=self.http_request_params['id']
            Lb.lobbyMessage(websocket=self)


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
        except Exception as ex:
            print(ex)
            print("An exception occurred, try again ")

        # print (listOfQ)

    def onClose(self, was_clean, code, reason):
        print("closed")
        st = self.http_request_uri.split("?")[0]
        if st == "/game":
           if   rocky.USERS.removeFromRoom(self):
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
