#!/bin/python3
import json

import TrumpHandler
from user import Gamer
from user import UserList


class rocky(object):
    def __init__(self):
        self.listOfQ = []
        self.listOfC = []
        self.listOfF = []
        self.USERS = UserList()
        self.TrumpObjects = {}

    def register(self, websocket, key, room, seatNo):

        gamerObject = self.USERS.checkForkey(key)
        if (self.USERS.canEnterTheRoom(room, seatNo)):  ## Need to replace with sqllite logic
            print("Will add in room " + str(room))
        else:
            print("Room is full or invalid seat no ")
            return False

        if gamerObject:
            # print (user)
            print("user already in table")
            if websocket in self.USERS.ws:
                print("ok ")
            else:
                print("we will re assign the socket with new one ")
                gamerObject.websocket = websocket
                self.USERS.addGameroRomm(room, seatNo, gamerObject)
                self.USERS.ws.append(websocket)
                return True


        else:
            #username = ("P" + "___" + key)  ##  This will change to sqllite Actitivy in USerList Object  ## str( random.randint(9,7568)

            gamerObject = Gamer(key, key, websocket, room, seatNo) ## Will imporve the secuirty later , by checking for key and get email 
            self.USERS.addtoList(gamerObject)
            self.USERS.addGameroRomm(room, seatNo, gamerObject)
            return True


    def IsthereTrumpSession(self, websocket):
        try:
            print("IsthereTrumpSession   ")
            roomUsers = (self.USERS.getRoomDetails(websocket))
            print(roomUsers)
            if not roomUsers:
                return False
            r = roomUsers["room"]

            if r in self.TrumpObjects:

                gamer = self.USERS.getUserBywebSocket(websocket)
                if gamer:

                    playerHand = []
                    P0 = self.TrumpObjects[r]
                    for kk in P0.tt.orderofPlay:  ## gamer.userID --> player name in Trump Table object
                        if (kk.name) == gamer.userID:
                            kk.websocket = websocket
                            playerHand = kk.showHand()
                    # self.sendCard(P0)
                    RR = self.TrumpObjects[r].rules

                    # self.TrumpIsSet({"villi":str (RR.villi),"trump":RR.trump,"dude":RR.dude,"dudeTeam":RR.Dudeteam})
                    # self.roomInfo(roomUsers['gamersInRomm'])
                    if RR.TrumpSet:
                        reconnectMessage = {"villi": str(RR.villi), 'trump': RR.trump, 'dude': RR.dude,
                                            'dudeTeam': RR.Dudeteam, 'hand': playerHand, 'VSF': [],
                                            "playsofar": P0.thisPlayForSunu}
                    else:
                        reconnectMessage = {"villi": str(RR.villi), 'trump': RR.trump, 'dude': RR.dude,
                                            'dudeTeam': RR.Dudeteam, 'hand': playerHand, 'VSF': RR.VSF,
                                            "playsofar": P0.thisPlayForSunu}

                    for kk in (self.listOfQ):
                        if kk['usr'] == gamer.userID:
                            message = {"event": "question", "usr": kk["usr"], "t": kk["t"], "quNo": kk["quNo"],
                                       "c": kk["c"], "r": kk["r"], "SN": kk["SN"], "VSF": kk["VSF"],
                                       "loopStart": kk["loopStart"]}
                            self.listOfQ.remove(kk)
                            message.update(reconnectMessage)
                            self.askQustion(message, gamer)
                            return True

                    for kk in (self.listOfC):
                        if kk['usr'] == gamer.userID:
                            message = {"event": "play", "hand": playerHand, "usr": kk["usr"], "pid": kk["pid"],
                                       "t": kk["t"], "playsofar": kk["playsofar"], "c": kk["c"], "r": kk["r"],
                                       "SN": kk["SN"]}
                            self.listOfC.remove(kk)
                            message.update(reconnectMessage)
                            self.askCard(message, gamer)
                            return True
                    for kk in (self.listOfF):
                        if kk['usr'] == gamer.userID:
                            message = {"event": "fold", "hand": playerHand, "usr": kk["usr"], "fid": kk["fid"],
                                       "r": kk["r"], "SN": kk["SN"]}
                            self.listOfF.remove(kk)
                            message.update(reconnectMessage)
                            self.askFold(message, gamer)
                            return True

                    reconnectMessage.update({"event": "Reconnect"})
                    payload = json.dumps(reconnectMessage).encode('utf8')
                    self.mySendMessage(websocket, payload)


                else:
                    print("ERROR:2033 BAD error ")
                return True
            else:
                False
        except Exception as ex:
            print(ex)
            print("Reconect Exception  ")

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

    def roomInfo(self, gamers):
        d = {}
        for kk in gamers:
            if kk is None:
                continue
            d["SN" + str(kk.seatNo + 1)] = kk.userID

        for kk in gamers:
            if kk is None:
                continue
            payload = json.dumps({"event": "seatInfo", "message": d}).encode('utf8')
            if kk.websocket:
                self.mySendMessage(kk.websocket, payload)

    def playSoFar(self, message, th):  ## This will change as per Room Logic

        payload = json.dumps({"event": "cardPlay", "playsofar": message["playsofar"]}).encode('utf8')
        for c in th.tt.orderofPlay:
            if c == None:
                continue
            if c.websocket:
                self.mySendMessage(c.websocket, payload)

    def heCalled(self, message, gamers):  ## This will change as per Room Logic

        payload = json.dumps(
            {"event": "HeCalled", "seat": message["seat"], "Villi": message["Villi"], "VSF": message["VSF"]}).encode(
            'utf8')
        for c in gamers:
            if c == None:
                continue
            if c.websocket:
                self.mySendMessage(c.websocket, payload)

    def heGotPidi(self, gamers, skip):  ## This will change as per Room Logic

        for c in gamers:
            if c == None:
                continue

            if c.websocket:
                payload = json.dumps({"event": "HeGotPidi", "who": (skip.seatNo), "my": (c.seatNo),
                                      "spinner": (skip.seatNo + 6 - c.seatNo) % 6}).encode('utf8')
                self.mySendMessage(c.websocket, payload)

    def sendCard(self, th):  ## This will change as per Room Logic
        # payload = json.dumps({"event":"broadcast","message":message}).encode('utf8')
        for kk in th.tt.orderofPlay:
            if kk == None:
                continue
            if kk.websocket:
                payload = json.dumps({"event": "cardSend", "hand": kk.hand}).encode('utf8')
                # payload = json.dumps({"event":"cardSend","cards":kk.showHandinUTF()}).encode('utf8')
                self.mySendMessage(kk.websocket, payload)

    def askQustion(self, message, client):
        payload = json.dumps(message).encode('utf8')
        # client.websocket.sendMessage(payload,False)
        self.mySendMessage(client.websocket, payload)
        self.listOfQ.append(
            {"quNo": message["quNo"], "status": "Asked", "ans": "", "usr": message["usr"], "t": message["t"],
             "c": message["c"], "r": message["r"], "SN": message["SN"], "VSF": message["VSF"],
             "loopStart": message["loopStart"]})
        print("Question1 Asked")

    def askCard(self, message, client):
        payload = json.dumps(message).encode('utf8')
        # client.websocket.sendMessage(payload,False)
        self.mySendMessage(client.websocket, payload)
        self.listOfC.append({"pid": message["pid"], 'playsofar': message['playsofar'], "status": "Asked", "card": "",
                             "usr": message["usr"], "t": message["t"], "c": message["c"], "r": message["r"],
                             "SN": message["SN"]})
        print("Card  Asked")

    def askFold(self, message, client):
        payload = json.dumps(message).encode('utf8')
        self.mySendMessage(client.websocket, payload)
        self.listOfF.append(
            {"fid": message["fid"], "status": "Asked", "usr": message["usr"], "r": message["r"], "SN": message["SN"]})
        print("Card  Asked")

    def canWeStart(self, websocket):
        roomUsers = (self.USERS.getRoomDetails(websocket))
        print(roomUsers)
        self.roomInfo(roomUsers['gamersInRomm'])
        if not roomUsers:
            print("ERROR:2002 Issue while registring room and users__")
            websocket.sendMessage("{'message':'Can't find room '}".encode('utf8'), False)
            return False

        r = roomUsers['room']
        if not None in roomUsers['gamersInRomm']:  ## Need to change to Room logic .

            th = TrumpHandler.TrumpHandler(roomUsers['gamersInRomm'])
            th.doTheDeal()
            th.tt.getOrderOfPlayers()
            self.TrumpObjects[r] = th
            self.MatchIsDone({"won": "", "base0": 5, "base1": 5, "dialoge": "", "Mc": 0, "KunuguSeat": []},
                             roomUsers['gamersInRomm'])
            self.sendCard(th)
            quNO = "R" + str(r) + str(0)
            P0 = th.tt.orderofPlay[0]
            villiSoFar = [{"S" + str(P0.seatNo): ""}]
            message = {"event": "question", "usr": P0.name, "SN": P0.seatNo, "t": "Team0", "quNo": quNO, "c": 0, "r": r,
                       "VSF": villiSoFar, "loopStart": 28}
            self.askQustion(message, P0)
            self.whoIsSpinner(th.tt.orderofPlay, P0)

        else:

            self.boradCast("Room: " + str((roomUsers['room'])) + " need " + str(roomUsers['gamersInRomm'].count(None)),
                           roomUsers['gamersInRomm'])

    def getAnswerOfOldquestion(self, AnsNo):
        obj = ""
        for kk in self.listOfQ:
            if kk['status'] == "DONE" and kk["quNo"] == AnsNo:
                obj = kk
                break
        self.listOfQ.remove(obj)
        return (kk)

    def getCardOfRequest(self, pid):
        obj = ""
        for kk in self.listOfC:
            if kk['status'] == "DONE" and kk["pid"] == pid:
                obj = kk
                break
        self.listOfC.remove(obj)
        return (kk)

    def managePlay(self, pid):
        lastCard = self.getCardOfRequest(pid)
        print(lastCard)
        r = lastCard["r"]
        seat = "S" + str(lastCard["SN"])
        RR = self.TrumpObjects[r].rules
        TT = self.TrumpObjects[r].tt
        self.TrumpObjects[r].thisPlayForSunu.append({seat: lastCard["card"]})
        self.TrumpObjects[r].thisPlay.append(lastCard["card"])
        PlaySoFar = self.TrumpObjects[r].thisPlay
        c = lastCard["c"]  ## --> Order of Index
        TT.orderofPlay[c].removeCard(lastCard["card"])
        self.playSoFar({"playsofar": self.TrumpObjects[r].thisPlayForSunu}, self.TrumpObjects[r])
        if len(PlaySoFar) == 6:
            print("Will check who got it ")
            print(PlaySoFar)
            if RR.IsTrumpInPlay(PlaySoFar):
                print("Trump Round")
                newC = RR.trumpInAction(PlaySoFar)

            else:
                newC = RR.whoIsLeader(PlaySoFar)
            team = TT.orderofPlay[newC].team
            print(newC)
            print(team)
            self.TrumpObjects[r].thisPlay = []
            self.TrumpObjects[r].thisPlayForSunu = []
            if team == "Team0":
                RR.t0Pidi.append(PlaySoFar)
            else:
                RR.t1Pidi.append(PlaySoFar)
            TT.opener = newC
            TT.getOrderOfPlayers()
            self.heGotPidi(TT.orderofPlay, TT.orderofPlay[
                (c + 1) % 6])  ## Need to send my seat also & dummy one . it should sending after win or not

            PlaySoFar = []  ### To prevent 6 cards in second play
            TTO = TT.orderofPlay[(c + 1) % 6]
            if self.didHeWon(RR, TT):
                print("match is over ")
                TTO = TT.orderofPlay[(c + 1) % 6]
                # {"fid":message["fid"],"status":"Asked","usr":message["usr"],"r":message["r"],"SN":message["SN"]}
                message = {"event": "fold", "usr": TTO.name, "fid": lastCard["pid"][:2], "t": TTO.team, "r": r,
                           "SN": TTO.seatNo}
                self.askFold(message, TTO)
                self.startNextMatch(r, False)
                return True

        TTO = TT.orderofPlay[(c + 1) % 6]
        pid = lastCard["pid"][:2] + str(int(lastCard["pid"][2:]) + 1)
        message = {"event": "play", "hand": TTO.showHand(), "usr": TTO.name, "pid": pid, "t": TTO.team,
                   "playsofar": self.TrumpObjects[r].thisPlayForSunu, "c": (c + 1) % 6, "r": r, "SN": TTO.seatNo}
        self.askCard(message, TTO)
        self.whoIsSpinner(TT.orderofPlay, TTO)

    def startNextMatch(self, r, okFromUI):
        if okFromUI:
            RR = self.TrumpObjects[r].rules
            TT = self.TrumpObjects[r].tt
            TT.VSF = [{}]
            RR.TrumpSet = False
            TT.setNextGame()
            TT.getOrderOfPlayers()
            self.TrumpObjects[r].doTheDeal()
            self.sendCard(self.TrumpObjects[r])
            quNO = "R" + str(r) + str(0)
            P0 = TT.orderofPlay[0]
            message = {"event": "question", "usr": P0.name, "t": P0.team, "SN": P0.seatNo, "quNo": quNO, "c": 0, "r": r,
                       "VSF": [], "loopStart": 28}
            self.askQustion(message, self.TrumpObjects[r].tt.orderofPlay[0])
            self.whoIsSpinner(self.TrumpObjects[r].tt.orderofPlay, self.TrumpObjects[r].tt.orderofPlay[0])
        else:
            print("Need to wait for ok from UI ")

    def didHeWon(self, rules, tt):
        t0P = rules.getPoints(rules.t0Pidi)
        t1P = rules.getPoints(rules.t1Pidi)
        print('Team0  ' + str(t0P))
        print('Team1  ' + str(t1P))
        if rules.t1GetPoint:
            if rules.villi <= t1P:
                dialoge = ("Team1 won  Villichu Jayichu so Just one base")
                tt.t1VillichuWon(rules.villi, rules.dudeSeatNo)
                message = {"won": "Team1", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                self.MatchIsDone(message, tt.orderofPlay)

                return True
            if (56 - rules.villi) < t0P:
                dialoge = ("Team0 won by Defending---- Give me two base")
                tt.t1VillichuLoss(rules.villi)
                message = {"won": "Team0", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                self.MatchIsDone(message, tt.orderofPlay)
                return True
        else:
            if rules.villi <= t0P:
                dialoge = ("Team0 won Villichu Jayichu so Just one base ")
                tt.t0VillichuWon(rules.villi, rules.dudeSeatNo)
                message = {"won": "Team0", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                self.MatchIsDone(message, tt.orderofPlay)
                return True
            if (56 - rules.villi) < t1P:
                dialoge = ("Team1 won by Defending---- Give me two base")
                tt.t0VillichuLoss(rules.villi)
                message = {"won": "Team1", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                self.MatchIsDone(message, tt.orderofPlay)
                return True
        return False

    def manageVilli(self, AnsNo):
        lastVilli = self.getAnswerOfOldquestion(AnsNo)
        r = lastVilli["r"]
        gamers = self.USERS.listOfRooms[r]
        RR = self.TrumpObjects[r].rules
        TT = self.TrumpObjects[r].tt
        c = lastVilli["c"]
        seat = "S" + str(lastVilli["SN"])
        RR.VSF.append({seat: lastVilli["ans"]})
        print(RR.VSF)
        message = {"seat": seat, "Villi": lastVilli["ans"], "VSF": RR.VSF}
        self.heCalled(message, gamers)
        if lastVilli["ans"] == "P":
            RR.skipped.add(lastVilli["usr"])
            if len(RR.skipped) == 6:  ## Need to change for 6
                print(RR.villi)
                RR.TrumpSet = True
                self.TrumpIsSet({"villi": str(RR.villi), "trump": RR.trump, "dude": RR.dude, "dudeTeam": RR.Dudeteam},
                                TT.orderofPlay)
                if RR.Dudeteam == "Team1":
                    RR.t1GetPoint = True
                else:
                    RR.t1GetPoint = False
                pid = "R" + str(r) + str(1)
                ##self.sendCard(self.TrumpObjects[r])   ## Not need
                message = {"event": "play", "hand": TT.orderofPlay[0].showHand(), "usr": TT.orderofPlay[0].name,
                           "pid": pid, "t": "Team0", "playsofar": [], "c": 0, "r": r, "SN": TT.orderofPlay[0].seatNo}
                self.askCard(message, TT.orderofPlay[0])
                self.whoIsSpinner(TT.orderofPlay, TT.orderofPlay[0])
                return True
        else:
            RR.villi = int(lastVilli["ans"][1:])
            RR.trump = lastVilli["ans"][0]
            RR.dude = lastVilli["usr"]
            RR.dudeSeatNo = lastVilli["SN"]
            RR.Dudeteam = lastVilli["t"]
        quNo = lastVilli["quNo"][:2] + str(int(lastVilli["quNo"][2:]) + 1)
        TTO = TT.orderofPlay[(c + 1) % 6]
        message = {"event": "question", "usr": TTO.name, "t": TTO.team, "quNo": quNo, "c": (c + 1) % 6, "r": r,
                   "SN": TTO.seatNo, "VSF": RR.VSF, "loopStart": RR.villi + 1}
        self.askQustion(message, TTO)
        self.whoIsSpinner(TT.orderofPlay, TTO)

    def whoIsSpinner(self, gamers, skip):
        #    message={"event":"spinner","spinner":skip.seatNo}

        for c in gamers:
            if c == None:
                continue
            if c.seatNo == skip.seatNo:
                continue
            if c.websocket:
                # message.update({"myseat":c.seatNo})  skip.seatNo  ( skip.seatNo+6-c.seatNo)%6
                payload = json.dumps({"event": "spinner", "spinner": (skip.seatNo + 6 - c.seatNo) % 6}).encode('utf8')
                self.mySendMessage(c.websocket, payload)

    def TrumpIsSet(self, message, gamers):  ## This will change as per Room Logic

        payload = json.dumps(
            {"event": "TrumpIsSet", "villi": message["villi"], "trump": message["trump"], "dude": message["dude"],
             "dudeTeam": message["dudeTeam"]}).encode('utf8')
        for c in gamers:
            if c == None:
                continue
            if c.websocket:
                self.mySendMessage(c.websocket, payload)

    def MatchIsDone(self, message, gamers):
        payload = json.dumps(
            {"event": "MatchIsDone", "won": message["won"], "base0": message["base0"], "base1": message["base1"],
             "dialoge": message["dialoge"], "Mc": message["Mc"], "KunuguSeat": message["KunuguSeat"]}).encode('utf8')
        for c in gamers:
            if c == None:
                continue
            if c.websocket:
                self.mySendMessage(c.websocket, payload)