#!/bin/python3
import asyncio
import json,random,time
import sys

from autobahn.asyncio.websocket import WebSocketClientProtocol, WebSocketClientFactory



class MyClientProtocol(WebSocketClientProtocol):

    done = asyncio.get_event_loop().create_future()

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))

    def onOpen(self):
        #self.sendMessage(u"Hello, world!".encode('utf8'))
        print("open")
        message="bot connected"
        payload = json.dumps({"event":"botConnection","message":message}).encode('utf8')
        self.sendMessage(payload)

    def onMessage(self, payload, isBinary):
        #print (payload)
        object=json.loads(payload)
        print (object)
        if (object['event'] == "question"):
            payload = json.dumps({"AnsNo":object["quNo"],"Answer":"P","usr":object["usr"],"t":object["t"]}).encode('utf8')
            time.sleep(1)
            self.sendMessage(payload)
            ## {"AnsNo":quNo,"Answer":data.value,"usr":obj.usr,"t":obj.t}
        if (object['event'] == "fold"):
                payload = json.dumps({"fid":object["fid"],"FR":"P","usr":object["usr"],"r":object["r"]}).encode('utf8')
                time.sleep(1)
                self.sendMessage(payload)

        if (object['event'] == "play"):
            time.sleep(1)
            ## {"pid":pid,"card":data.value,"usr":obj.usr,"t":obj.t}
            card=""
            print (object['playsofar'])
            if   len (object['playsofar']) > 0:  ## Checking empty dictonry

                for kk in object['playsofar'][0]:
                    FirstCard=object['playsofar'][0][kk][0]
                print (FirstCard)
                res = [idx for idx in object['hand'] if idx.startswith(FirstCard)]
                if len (res) > 0:
                    card= random.choice(res)
                else:
                    card= random.choice(object['hand'])
            else:
                card=random.choice(object['hand'])

            payload = json.dumps( {"pid":object['pid'],"card":card,"usr":object["usr"],"t":object["t"]}).encode('utf8')
            self.sendMessage(payload)



    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))




if __name__ == '__main__':
    print (sys.argv)
    if len (sys.argv) == 2:
        factory = WebSocketClientFactory(sys.argv[1])
    else:
        print ('pass the url like "ws://127.0.0.1:6789/key=bot1&Room=0&seatN0=2"               it should pass in qute' )
        quit()
        factory = WebSocketClientFactory("ws://127.0.0.1:6789/key="+sys.argv[1]+"&Room=0")
    factory.protocol = MyClientProtocol
    loop = asyncio.get_event_loop()
    async def main():
        coro = loop.create_connection(factory, "3.17.191.219", 6789)
        print("running {}".format(coro))
        transport, proto = await coro
        print("proto {}".format(proto))
        await proto.done
    loop.run_until_complete(main())
    loop.close()


#./aws_bot.py "ws://3.17.191.219:6789/key=bot1&Room=0&seatN0=1"
# ./aws_bot.py "ws://3.17.191.219:6789/key=bot2&Room=0&seatN0=2"
# ./aws_bot.py "ws://3.17.191.219:6789/key=bot3&Room=0&seatN0=3"
# ./aws_bot.py "ws://3.17.191.219:6789/key=bot4&Room=0&seatN0=4"
# ./aws_bot.py "ws://3.17.191.219:6789/key=bot5&Room=0&seatN0=5"
# ./aws_bot.py "ws://3.17.191.219:6789/key=bot6&Room=0&seatN0=6"
