#!/bin/python3
import asyncio
import logging
import json
from user import Gamer
from user import UserList
from manageMessage import rocky

from autobahn.asyncio.websocket import (WebSocketServerProtocol,WebSocketServerFactory)



logging.basicConfig(level=logging.INFO)
rocky=rocky()



class ChatProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        try :

            key=(request.path.split("=")[1])
            #print (key)
            rocky.register(self,key)

        except Exception as ex:
                    print (ex)
                    print("An exception occurred, will not be registered ")



    def onOpen(self):

        room=0
        rocky.canWeStart(room)




    def onMessage(self, payload, is_binary):
        print (payload)
        object=json.loads(payload)
        print (rocky.listOfQ)
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
        rocky.USERS.ws.remove(self)





if __name__ == "__main__":
    factory = WebSocketServerFactory("ws://localhost:6789")
    factory.protocol = ChatProtocol

    loop = asyncio.get_event_loop()
    asyncio.Task(loop.create_server(factory, port=6789))
    loop.run_forever()
