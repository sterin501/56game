#!/bin/python3
import json




class Parava(object):
    def __init__(self):
        pass

    def mySendMessage(self, websocket, payload):
            try:
                websocket.sendMessage(payload, False)
                return True
            except Exception as ex:
                print(ex)
                print("CODE:2012 Can't sendMessage to client")
            return False

    def boradCast(self, message, gamers):  ## This will change as per Room Logic
            payload = json.dumps({"event": "broadcast", "message": message}).encode('utf8')
            for c in gamers:
                if c == None:
                    continue
                if c.websocket:
                    self.mySendMessage(c.websocket, payload)

    def roomInfo(self, gamers,skip,kunugulist,watchlist):
                        print (gamers)
                        d = {}
                        seatNo=0
                        for kk in gamers:
                            seatNo=seatNo+1

                            if kk is None:
                                d["SN" + str(seatNo)] = "Empty"   ## Sending  Empty to avoid undefined
                                continue
                            d["SN" + str(seatNo)] = kk.userID
                        wl=[]
                        for kk in   watchlist:
                                wl.append (kk.http_request_params['id'][0])

                        payload = json.dumps({"event": "seatInfo", "names": d,"KunuguSeat":kunugulist,"watchlist":wl}).encode('utf8')
                        for kk in gamers:
                            if kk is None:
                                continue
                            if kk == skip:
                                continue
                            if kk.websocket:
                                self.mySendMessage(kk.websocket, payload)
                        for kk in   watchlist:
                            self.mySendMessage(kk,payload)

    def playSoFar(self, message, th,watchlist):  ## This will change as per Room Logic
                        payload = json.dumps({"event": "cardPlay", "playsofar": message["playsofar"]}).encode('utf8')
                        for c in th.tt.orderofPlay:
                            if c == None:
                                continue
                            if c.websocket:
                                self.mySendMessage(c.websocket, payload)
                        for kk in   watchlist:
                                        self.mySendMessage(kk,payload)



    def heCalled(self, message, gamers,watchlist):  ## This will change as per Room Logic
                                    payload = json.dumps(
                                        {"event": "HeCalled", "seat": message["seat"], "Villi": message["Villi"], "VSF": message["VSF"],"dude":message["dude"],"dudeTeam":message["dudeTeam"]}).encode(
                                        'utf8')
                                    for c in gamers:
                                        if c == None:
                                            continue
                                        if c.websocket:
                                            self.mySendMessage(c.websocket, payload)
                                    for kk in   watchlist:
                                                                self.mySendMessage(kk,payload)

    def heGotPidi(self, gamers, skip,watchlist):  ## This will change as per Room Logic
                                    for c in gamers:
                                        if c == None:
                                            continue

                                        if c.websocket:
                                            payload = json.dumps({"event": "HeGotPidi", "who": (skip.seatNo), "my": (c.seatNo),
                                                                  "spinner": (skip.seatNo + 6 - c.seatNo) % 6}).encode('utf8')
                                            self.mySendMessage(c.websocket, payload)

                                    payload = json.dumps({"event": "HeGotPidi", "who": (skip.seatNo), "my": (1),
                                                          "spinner": (skip.seatNo + 6 - 1) % 6}).encode('utf8')
                                    for kk in   watchlist:
                                                        self.mySendMessage(kk,payload)


    def sendCard(self, th):  ## This will change as per Room Logic
                                    for kk in th.tt.orderofPlay:
                                        if kk == None:
                                            continue
                                        if kk.websocket:
                                            payload = json.dumps({"event": "cardSend", "hand": kk.hand}).encode('utf8')
                                            # payload = json.dumps({"event":"cardSend","cards":kk.showHandinUTF()}).encode('utf8')
                                            self.mySendMessage(kk.websocket, payload)


    def whoIsSpinner(self, gamers, skip,watchlist):
                                                for c in gamers:
                                                    if c == None:
                                                        continue
                                                    if c.seatNo == skip.seatNo:
                                                        continue
                                                    if c.websocket:
                                                        # message.update({"myseat":c.seatNo})  skip.seatNo  ( skip.seatNo+6-c.seatNo)%6
                                                        payload = json.dumps({"event": "spinner", "spinner": (skip.seatNo + 6 - c.seatNo) % 6}).encode('utf8')
                                                        self.mySendMessage(c.websocket, payload)

                                                payload = json.dumps({"event": "spinner", "spinner": (skip.seatNo + 6 - 1) % 6}).encode('utf8')
                                                for kk in   watchlist:
                                                            self.mySendMessage(kk,payload)



    def TrumpIsSet(self, message, gamers,watchlist):
                                                            payload = json.dumps(
                                                                {"event": "TrumpIsSet", "villi": message["villi"], "trump": message["trump"], "dude": message["dude"],
                                                                 "dudeTeam": message["dudeTeam"]}).encode('utf8')
                                                            for c in gamers:
                                                                if c == None:
                                                                    continue
                                                                if c.websocket:
                                                                    self.mySendMessage(c.websocket, payload)
                                                            for kk in   watchlist:
                                                                self.mySendMessage(kk,payload)


    def MatchIsDone(self, message, gamers,watchlist):
                                                                        payload = json.dumps(
                                                                            {"event": "MatchIsDone", "won": message["won"], "base0": message["base0"], "base1": message["base1"],
                                                                             "dialoge": message["dialoge"], "Mc": message["Mc"], "KunuguSeat": message["KunuguSeat"]}).encode('utf8')
                                                                        for c in gamers:
                                                                            if c == None:
                                                                                continue
                                                                            if c.websocket:
                                                                                self.mySendMessage(c.websocket, payload)

                                                                        for kk in   watchlist:
                                                                                            self.mySendMessage(kk,payload)


    def  chatSend(self,message,gamers,watchlist):
        payload = json.dumps(message).encode('utf8')
        for c in gamers:
            if c == None:
                continue
            if c.websocket:
                self.mySendMessage(c.websocket, payload)

        for kk in   watchlist:
                self.mySendMessage(kk,payload)
