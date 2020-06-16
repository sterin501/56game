#!/usr/bin/python3
import asyncio
import logging
import json

from manageMessage import rocky
from autobahn.asyncio.websocket import (WebSocketServerProtocol,WebSocketServerFactory)



logging.basicConfig(level=logging.INFO)
print ("Creating user object ")
rocky=rocky()



class ChatProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        try :

            st=(request.path.split("/")[1])
            #print (st)
            key=st.split("&")[0].split("=")[1]
            room=int (st.split("&")[1].split("=")[1]) ## starts with zero only
            seat=int (st.split("&")[2].split("=")[1])
            seat=seat-1                              ## for array
            print (key,room)
            rocky.register(self,key,room,seat)
            print (self.http_headers)

        except Exception as ex:
                    print (ex)
                    print("An exception occurred, will not be registered ")



    def onOpen(self):
        if  rocky.IsthereTrumpSession(websocket=self):
            print (" Reconect ")
        else:
            rocky.canWeStart(websocket=self)




    def onMessage(self, payload, is_binary):
        print (payload)
        object=json.loads(payload)
        # (rocky.listOfQ)
        ##  {"pid":pid,"card":data.value,"usr":obj.usr,"t":obj.t}  for Card Play
        ##  {"AnsNo":4,"Answer":"P","usr":"P1","t":"Team0"}'       for Villi Logic
        if  'AnsNo' in object:

            AnsNo=object['AnsNo']
            for kk in rocky.listOfQ:
                if kk['quNo'] == AnsNo:
                    print ("inside AnsNo iffff")
                    kk['status'] = 'DONE'
                    kk['ans']= object['Answer']
                    rocky.manageVilli(AnsNo)
        elif 'pid' in object:
            pid=object['pid']
            for kk in rocky.listOfC:

                if kk['pid'] == pid:
                    print ("Card iffff")
                    kk['status'] = "DONE"
                    kk['card'] = object['card']
                    rocky.managePlay(pid)


        #print (listOfQ)


    def onClose(self, was_clean, code, reason):
        print ("closed")
        rocky.USERS.removeFromRoom(self)
        #rocky.USERS.ws.remove(self)                ## Removed from active Websockets





if __name__ == "__main__":
    print ("Listening on 6789")
    factory = WebSocketServerFactory("ws://localhost:6789")
    factory.protocol = ChatProtocol

    loop = asyncio.get_event_loop()
    asyncio.Task(loop.create_server(factory, port=6789))
    loop.run_forever()
