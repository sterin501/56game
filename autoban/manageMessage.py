#!/bin/python3
import json

import TrumpHandler
from user import Gamer
from user import UserList
from parava import Parava

PV=Parava()


class rocky(object):
    def __init__(self):
        self.listOfQ = []
        self.listOfC = []
        self.listOfF = []
        self.USERS = UserList()
        self.TrumpObjects = {}
        self.resetList=[]

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
            print (str (room) + "<-->"+ str (seatNo))
            gamerObject = Gamer(key, key, websocket, room, seatNo) ## Will imporve the secuirty later , by checking for key and get email
            self.USERS.addtoList(gamerObject)
            self.USERS.addGameroRomm(room, seatNo, gamerObject)
            return True

    def unregister(self,websocket,room,seat):
        if self.USERS.removeFromRoom(websocket):
            if room in self.TrumpObjects:
                th=self.TrumpObjects[room]
                if th.P1.seatNo==seat:
                    th.P1.vacant=True
                elif th.P2.seatNo==seat:
                        print (th.P2.name)
                        th.P2.vacant=True
                elif th.P3.seatNo==seat:
                        th.P3.vacant=True
                elif th.P4.seatNo==seat:
                        th.P4.vacant=True
                elif th.P5.seatNo==seat:
                        th.P5.vacant=True
                elif th.P6.seatNo==seat:
                        th.P6.vacant=True
            Room=self.USERS.listOfRooms[room]
            PV.roomInfo(Room,False)
            print (str (room )+ "::" + str (seat) + "  free")
            return True



    def IsthereTrumpSession(self, websocket,room,seat):
        try:
            print("IsthereTrumpSession??   ")
            #roomUsers = (self.USERS.getRoomDetails(websocket))
            Room=self.USERS.listOfRooms[room]
            if not Room:
                return False
            r = room
            if r in self.TrumpObjects:
                gamer = self.USERS.getUserBywebSocket(websocket)
                if gamer:
                    playerHand = []
                    P0 = self.TrumpObjects[r]
                    playerInRoom=P0.getPlayerBySeat(seat)
                    if not playerInRoom:
                        print ("Still it is NOT vacant  " + str (seat))
                        return False
                    playerInRoom.name=gamer.userID
                    playerInRoom.websocket=websocket
                    playerInRoom.vacant=False
                    playerHand = playerInRoom.showHand()
                    print ("Reconnected  fine  "+ str (playerInRoom.__dict__) )
                    PV.roomInfo(Room,gamer)
                    RR = self.TrumpObjects[r].rules
                    d = {}
                    for we  in range(1,7):
                        P=P0.tt.getPlayerName("P"+str(we))
                        d["SN" + str(we)] = P

                    if RR.TrumpSet:
                        reconnectMessage = {"villi": str(RR.villi), 'trump': RR.trump, 'dude': RR.dude,
                                            'dudeTeam': RR.Dudeteam, 'hand': playerHand, 'VSF': [],
                                            "playsofar": P0.thisPlayForSunu,"names":d,"base0":P0.tt.t0base,"base1":P0.tt.t1base,"Mc":P0.tt.gameCount,"KunuguSeat":P0.tt.listOfKunugu}
                    else:
                        reconnectMessage = {"villi": str(RR.villi), 'trump': RR.trump, 'dude': RR.dude,
                                            'dudeTeam': RR.Dudeteam, 'hand': playerHand, 'VSF': RR.VSF,
                                            "playsofar": P0.thisPlayForSunu,"names":d,"base0":P0.tt.t0base,"base1":P0.tt.t1base,"Mc":P0.tt.gameCount,"KunuguSeat":P0.tt.listOfKunugu}

                    for kk in (self.listOfQ):
                        if kk['SN'] == gamer.seatNo+1:
                            message = {"event": "question", "usr": kk["usr"], "t": kk["t"], "quNo": kk["quNo"],
                                       "c": kk["c"], "r": kk["r"], "SN": kk["SN"], "VSF": kk["VSF"],
                                       "loopStart": kk["loopStart"]}
                            self.listOfQ.remove(kk)
                            message.update(reconnectMessage)
                            self.askQustion(message, gamer)
                            return True

                    for kk in (self.listOfC):
                        if kk['SN'] == gamer.seatNo+1:
                            message = {"event": "play", "hand": playerHand, "usr": kk["usr"], "pid": kk["pid"],
                                       "t": kk["t"], "playsofar": kk["playsofar"], "c": kk["c"], "r": kk["r"],
                                       "SN": kk["SN"]}
                            self.listOfC.remove(kk)
                            message.update(reconnectMessage)
                            self.askCard(message, gamer)
                            return True
                    for kk in (self.listOfF):
                        if kk['SN'] == gamer.seatNo+1:
                            message = {"event": "fold", "hand": playerHand, "usr": kk["usr"], "fid": kk["fid"],
                                       "r": kk["r"], "SN": kk["SN"]}
                            self.listOfF.remove(kk)
                            message.update(reconnectMessage)
                            self.askFold(message, gamer)
                            return True

                    reconnectMessage.update({"event": "Reconnect"})
                    payload = json.dumps(reconnectMessage).encode('utf8')
                    PV.mySendMessage(websocket, payload)


                else:
                    print("Gamer is not found .Not registered ")
                return True
            else:
                False
        except Exception as ex:
            print(ex)
            print("Reconect Exception  ")



    def askQustion(self, message, client):
        payload = json.dumps(message).encode('utf8')
        PV.mySendMessage(client.websocket, payload)
        self.listOfQ.append(
            {"quNo": message["quNo"], "status": "Asked", "ans": "", "usr": message["usr"], "t": message["t"],
             "c": message["c"], "r": message["r"], "SN": message["SN"], "VSF": message["VSF"],
             "loopStart": message["loopStart"]})
        print("Question1 Asked  " +  message["usr"])

    def askCard(self, message, client):
        payload = json.dumps(message).encode('utf8')
        PV.mySendMessage(client.websocket, payload)
        self.listOfC.append({"pid": message["pid"], 'playsofar': message['playsofar'], "status": "Asked", "card": "",
                             "usr": message["usr"], "t": message["t"], "c": message["c"], "r": message["r"],
                             "SN": message["SN"]})
        print("Card  Asked  "+ message["usr"])

    def askFold(self, message, client):
        payload = json.dumps(message).encode('utf8')
        PV.mySendMessage(client.websocket, payload)
        self.listOfF.append(
            {"fid": message["fid"], "status": "Asked", "usr": message["usr"], "r": message["r"], "SN": message["SN"]})
        print("Card  Asked "+message["usr"])

    def canWeStart(self, websocket,roomNo,seatNo):
        Room=self.USERS.listOfRooms[roomNo]
        PV.roomInfo(Room,False)
        if not Room:
            print("ERROR:2002 Issue while registring room and users__")
            websocket.sendMessage("{'message':'Can't find room '}".encode('utf8'), False)
            return False

        if not None in Room:  ## Need to change to Room logic .
            if roomNo in self.TrumpObjects:
                print ("Game started already wont restart this time ")
                return "Game already"
            th = TrumpHandler.TrumpHandler(Room)
            th.doTheDeal()
            th.tt.getOrderOfPlayers()
            self.TrumpObjects[roomNo] = th
            PV.MatchIsDone({"won": "", "base0": 5, "base1": 5, "dialoge": " starting ..", "Mc": 0, "KunuguSeat": []},
                             Room)
            PV.sendCard(th)
            quNO = "R" + str(roomNo) + str(0)
            P0 = th.tt.orderofPlay[0]
            villiSoFar = [{"S" + str(P0.seatNo): ""}]
            message = {"event": "question", "usr": P0.name, "SN": P0.seatNo, "t": "Team0", "quNo": quNO, "c": 0, "r": roomNo,
                       "VSF": villiSoFar, "loopStart": 28}
            self.askQustion(message, P0)
            PV.whoIsSpinner(th.tt.orderofPlay, P0)

        else:

            PV.boradCast("Room: " + str(roomNo) + " need " + str(Room.count(None)),
                           Room)

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
        PV.playSoFar({"playsofar": self.TrumpObjects[r].thisPlayForSunu}, self.TrumpObjects[r])
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
            PV.heGotPidi(TT.orderofPlay, TT.orderofPlay[
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
        PV.whoIsSpinner(TT.orderofPlay, TTO)

    def startNextMatch(self, r, okFromUI):
        if okFromUI:
            RR = self.TrumpObjects[r].rules
            TT = self.TrumpObjects[r].tt
            TT.VSF = [{}]
            RR.TrumpSet = False
            TT.setNextGame()
            TT.getOrderOfPlayers()
            self.TrumpObjects[r].doTheDeal()
            PV.sendCard(self.TrumpObjects[r])
            quNO = "R" + str(r) + str(0)
            P0 = TT.orderofPlay[0]
            message = {"event": "question", "usr": P0.name, "t": P0.team, "SN": P0.seatNo, "quNo": quNO, "c": 0, "r": r,
                       "VSF": [], "loopStart": 28}
            self.askQustion(message, self.TrumpObjects[r].tt.orderofPlay[0])
            PV.whoIsSpinner(self.TrumpObjects[r].tt.orderofPlay, self.TrumpObjects[r].tt.orderofPlay[0])
        else:
            print("Need to wait for ok from UI ")

    def didHeWon(self, rules, tt):
        t0P = rules.getPoints(rules.t0Pidi)
        t1P = rules.getPoints(rules.t1Pidi)
        print('Team0  ' + str(t0P))
        print('Team1  ' + str(t1P))
        if rules.t1GetPoint:
            if rules.villi <= t1P:
                dialoge = str(t0P)+"/"+str(t1P)+(" Red won  Villichu Jayichu so Just one base")
                tt.t1VillichuWon(rules.villi, rules.dudeSeatNo)
                message = {"won": "Team1", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                PV.MatchIsDone(message, tt.orderofPlay)

                return True
            if (56 - rules.villi) < t0P:
                dialoge =  str(t0P)+"/"+str(t1P)+(" Black won by Defending---- Give me two base")
                tt.t1VillichuLoss(rules.villi)
                message = {"won": "Team0", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                PV.MatchIsDone(message, tt.orderofPlay)
                return True
        else:
            if rules.villi <= t0P:
                dialoge = str(t0P)+"/"+str(t1P)+(" Black won Villichu Jayichu so Just one base ")
                tt.t0VillichuWon(rules.villi, rules.dudeSeatNo)
                message = {"won": "Team0", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                PV.MatchIsDone(message, tt.orderofPlay)
                return True
            if (56 - rules.villi) < t1P:
                dialoge = str(t0P)+"/"+str(t1P)+(" Red won by Defending---- Give me two base")
                tt.t0VillichuLoss(rules.villi)
                message = {"won": "Team1", "base0": tt.t0base, "base1": tt.t1base, "dialoge": dialoge,
                           "Mc": tt.gameCount, "KunuguSeat": tt.listOfKunugu}
                PV.MatchIsDone(message, tt.orderofPlay)
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
        if lastVilli["ans"] == "P":
            RR.skipped.add(lastVilli["usr"])
            if len(RR.skipped) == 6:  ## Need to change for 6
                print(RR.villi)
                RR.TrumpSet = True
                PV.TrumpIsSet({"villi": str(RR.villi), "trump": RR.trump, "dude": RR.dude, "dudeTeam": RR.Dudeteam},
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
                PV.whoIsSpinner(TT.orderofPlay, TT.orderofPlay[0])
                return True
        else:
            RR.villi = int(lastVilli["ans"][1:])
            RR.trump = lastVilli["ans"][0]
            RR.dude = lastVilli["usr"]
            RR.dudeSeatNo = lastVilli["SN"]
            RR.Dudeteam = lastVilli["t"]
        message = {"seat": seat, "Villi": lastVilli["ans"], "VSF": RR.VSF,"dude": RR.dude, "dudeTeam": RR.Dudeteam}
        PV.heCalled(message, gamers)
        quNo = lastVilli["quNo"][:2] + str(int(lastVilli["quNo"][2:]) + 1)
        TTO = TT.orderofPlay[(c + 1) % 6]
        message = {"event": "question", "usr": TTO.name, "t": TTO.team, "quNo": quNo, "c": (c + 1) % 6, "r": r,
                   "SN": TTO.seatNo, "VSF": RR.VSF, "loopStart": RR.villi + 1}
        self.askQustion(message, TTO)
        PV.whoIsSpinner(TT.orderofPlay, TTO)


    def resetBase(self,usr,room,seatNo):
        Room=self.USERS.listOfRooms[room]
        if  not (Room[seatNo].userID ==usr ):
            print ("Invalid player request to reset the game ")
            return False
        for kk in self.resetList:
            if room in kk:
                 if (kk[room]+seatNo)%2 ==1:
                      print ("going to reset for " + str (room+1))
                      TT = self.TrumpObjects[room].tt
                      TT.t0base=5
                      TT.t1base=5
                      TT.gameCount = 1
                      TT.listOfKunugu = []
                      TT.KunugSetAt=-1
                      TT.lastKunugTeam=""
                      PV.MatchIsDone({"won": "", "base0": 5, "base1": 5, "dialoge": "did Reset by " + str (kk[room])+"_"+ str(seatNo), "Mc": 0, "KunuguSeat": []},
                            Room)
                      self.resetList.remove(kk)
                      return True
        print (" Reset request for " + str (room) + "  "+ str(seatNo))
        d={}
        d[room]=seatNo
        self.resetList.append(d)


    def gotoLobby(self,usr,room,seatNo):
        Room=self.USERS.listOfRooms[room]
        if  not (Room[seatNo].userID ==usr ):
            print ("Invalid player request to reset the game ")
            return False
        if room in self.TrumpObjects:
                th=self.TrumpObjects[room]
                if th.P1.seatNo==seatNo+1:
                    th.P1.vacant=True
                elif th.P2.seatNo==seatNo+1:
                        print (th.P2.name)
                        th.P2.vacant=True
                elif th.P3.seatNo==seatNo+1:
                        th.P3.vacant=True
                elif th.P4.seatNo==seatNo+1:
                        th.P4.vacant=True
                elif th.P5.seatNo==seatNo+1:
                        th.P5.vacant=True
                elif th.P6.seatNo==seatNo+1:
                        th.P6.vacant=True
        self.USERS.listOfRooms[room][seatNo]=None                
        print ("send to lobby")
