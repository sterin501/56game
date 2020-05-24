#!/bin/python3
import asyncio
import json,random
from user import Gamer
from user import UserList
import TrumpHandler

from autobahn.asyncio.websocket import (WebSocketServerProtocol,WebSocketServerFactory)




class rocky(object):
    def __init__(self):
        self.listOfQ=[]
        self.listOfC=[]
        self.USERS=UserList()
        self.TrumpObjects={}

    def register(self,websocket,key,room):


                user=self.USERS.checkForkey(key)
                if (self.USERS.canEnterTheRoom("P"+ "___"+key,room)):  ## Need to replace with sqllite logic
                     print ("Will add in room " + str (room))
                else:
                    print ("Room is full ")
                    return False

                #print (user)
                if   user:
                     #print (user)
                     print ("user already in table")
                     if websocket in self.USERS.ws:
                         print ("ok ")
                     else:
                         print ("we will re assign ")
                         user.websocket=websocket

                else:
                    username=("P"+ "___"+key )  ##  This will change to sqllite Actitivy in USerList Object  ## str( random.randint(9,7568)
                    gamerObject=Gamer(username,key,websocket,room)
                    self.USERS.addtoList(gamerObject)
                    self.USERS.addGameroRomm(room,gamerObject)




    def IsthereTrumpSession(self,websocket):
        try:
         print ("IsthereTrumpSession   ")
         roomUsers=(self.USERS.getRoomDetails(websocket))
         print (roomUsers)
         if not roomUsers:
             return False
         r=roomUsers["room"]

         if   r in  self.TrumpObjects:

               gamer=self.USERS.getUserBywebSocket(websocket)
               if gamer:
                   for kk in self.TrumpObjects[r].tt.orderofPlay:   ## gamer.userID --> player name in Trump Table object
                       if (kk.name)==gamer.userID:
                           kk.websocket=websocket
                           playerHand=kk.showHand()
                   self.sendCard(self.TrumpObjects[r])
                   RR=self.TrumpObjects[r].rules
                   #self.TrumpIsSet({"villi":str (RR.villi),"trump":RR.trump,"dude":RR.dude,"dudeTeam":RR.Dudeteam})
                   payload = json.dumps({"event":"Reconnect","villi":str (RR.villi),'trump': RR.trump, 'dude': RR.dude, 'dudeTeam': RR.Dudeteam,'hand':playerHand}).encode('utf8')
                   #websocket.sendMessage(payload, False)
                   self.mySendMessage(websocket,payload)
                   for kk in  (self.listOfQ):
                       if kk['usr']==gamer.userID:
                           message={"event":"question","question":"what is your trump?","usr":kk["usr"],"t":kk["t"],"quNo":kk["quNo"],"c":kk["c"],"room":kk["room"]}
                           self.listOfQ.remove(kk)
                           self.askQustion(message,gamer)
                           return True

                   for kk in  (self.listOfC):
                               if kk['usr']==gamer.userID:
                                   #message={"event":"question","question":"what is your trump?","usr":kk["usr"],"t":kk["t"],"quNo":kk["quNo"],"c":kk["c"]}
                                   message={"event":"play","hand":playerHand,"usr":kk["usr"],"pid":kk["pid"],"t":kk["t"],"playsofar":kk["playsofar"],"c":kk["c"],"room":kk["room"] }
                                   self.listOfC.remove(kk)
                                   self.askCard(message,gamer)
                                   return True


               else:
                   print ("ERROR:2033 BAD error ")


               return True
         else:
            False
        except Exception as ex:
                    print (ex)
                    print ("Reconect check  ")


    def  mySendMessage(self,websocket,payload):
         try:
               websocket.sendMessage(payload, False)
               return True
         except Exception as ex:
                       print (ex)
                       print("CODE:2012 Can't sendMessage to client")
         return False


    def  boradCast(self,message,gamers):                            ## This will change as per Room Logic

                         payload = json.dumps({"event":"broadcast","message":message}).encode('utf8')
                         for c in gamers:
                              if c.websocket:
                                 self.mySendMessage(c.websocket,payload)



    def playSoFar(self,message,th):                            ## This will change as per Room Logic

                         payload = json.dumps({"event":"cardPlay","message":message["msg"],"playsofar":message["playsofar"]}).encode('utf8')
                         for c in th.tt.orderofPlay:
                              if c.websocket:
                                self.mySendMessage(c.websocket,payload)

    def  sendCard(self,th):                            ## This will change as per Room Logic
                         #payload = json.dumps({"event":"broadcast","message":message}).encode('utf8')
                          for kk in   th.tt.orderofPlay:
                                   if kk.websocket:
                                      payload = json.dumps({"event":"cardSend","hand":kk.hand}).encode('utf8')
                                      #payload = json.dumps({"event":"cardSend","cards":kk.showHandinUTF()}).encode('utf8')
                                      self.mySendMessage(kk.websocket,payload)



    def askQustion(self,message,client):
                            payload = json.dumps(message).encode('utf8')
                            #client.websocket.sendMessage(payload,False)
                            self.mySendMessage(client.websocket,payload)
                            self.listOfQ.append({"quNo":message["quNo"],"status":"Asked","ans":"","usr":message["usr"],"t":message["t"],"c":message["c"],"room":message["room"]})
                            print ("Question1 Asked")

    def askCard(self,message,client):
                            payload = json.dumps(message).encode('utf8')
                            #client.websocket.sendMessage(payload,False)
                            self.mySendMessage(client.websocket,payload)
                            self.listOfC.append({"pid":message["pid"],'playsofar':message['playsofar'],"status":"Asked","card":"","usr":message["usr"],"t":message["t"],"c":message["c"],"room":message["room"]})
                            print ("Card  Asked")

    def canWeStart(self,websocket):
                                  roomUsers=(self.USERS.getRoomDetails(websocket))
                                  print (roomUsers)
                                  if not roomUsers:
                                      print ("ERROR:2002 Issue while registring room and users__")
                                      websocket.sendMessage("{'message':'Can't find room '}".encode('utf8'), False)



                                  if not roomUsers:
                                      return False
                                  r=roomUsers['room']
                                  if len (roomUsers['gamersInRomm']) ==6:  ## Need to change to Room logic .

                                      th=TrumpHandler.TrumpHandler(roomUsers['gamersInRomm'])
                                      st=th.publicTextBeforeEveryMatch()+"  ....   ....  "
                                      th.doTheDeal()
                                      th.tt.getOrderOfPlayers()
                                      self.TrumpObjects[r]=th
                                      self.boradCast ({"event":"broadcast","message":st},roomUsers['gamersInRomm'])
                                      self.sendCard(th)
                                      quNO="R"+str(r)+str(0)
                                      message={"event":"question","question":"what is your trump?","usr":"P1","t":"Team0","quNo":quNO,"c":0,"room":r}
                                      self.askQustion(message,th.tt.orderofPlay[0])

                                  else:
                                      self.boradCast ("Room:"+str ((roomUsers['room'])) +" need " + str ( 6 - len (roomUsers['gamersInRomm'])),roomUsers['gamersInRomm'] )


    def getAnswerOfOldquestion(self,AnsNo):
                                  obj=""
                                  for kk in self.listOfQ:
                                      if kk['status'] == "DONE" and kk["quNo"] == AnsNo:
                                          obj=kk
                                          break
                                  self.listOfQ.remove(obj)
                                  return (kk)


    def getCardOfRequest(self,pid):
                             obj=""
                             for kk in self.listOfC:
                                 if kk['status'] == "DONE" and kk["pid"] == pid:
                                     obj=kk
                                     break
                             self.listOfC.remove(obj)
                             return (kk)
    def  managePlay(self,pid):
                            lastCard=self.getCardOfRequest(pid)
                            print(lastCard)
                            r=lastCard["room"]
                            RR=self.TrumpObjects[r].rules
                            TT=self.TrumpObjects[r].tt
                            self.TrumpObjects[r].thisPlay.append(lastCard["card"])
                            PlaySoFar=self.TrumpObjects[r].thisPlay
                            c=lastCard["c"]                  ## --> Order of Index
                            TT.orderofPlay[c].removeCard(lastCard["card"])
                            self.playSoFar({"msg":TT.orderofPlay[c].name+ "  played  "+ lastCard['card'], "playsofar":PlaySoFar},self.TrumpObjects[r])
                            if len(PlaySoFar) == 6:
                                print ("Will check who got it ")
                                print (PlaySoFar)
                                if RR.IsTrumpInPlay(PlaySoFar):
                                        print ("Trump Round")
                                        newC=RR.trumpInAction(PlaySoFar)

                                else:
                                        newC=RR.whoIsLeader(PlaySoFar)
                                team=TT.orderofPlay[newC].team
                                print (newC)
                                print (team)
                                self.TrumpObjects[r].thisPlay=[]
                                if team == "Team0":
                                             RR.t0Pidi.append(PlaySoFar)
                                else:
                                             RR.t1Pidi.append(PlaySoFar)
                                TT.opener=newC
                                TT.getOrderOfPlayers()
                                PlaySoFar=[]  ### To prevent 6 cards in second play
                                if self.didHeWon(RR,TT):
                                    print ("won")
                                    self.startNextMatch(r)
                                    return True



                            pid=lastCard["pid"][:2]+ str (int (lastCard["pid"][2:]) +1)
                            TTO=TT.orderofPlay[(c+1)%6]
                            message={"event":"play","hand":TTO.showHand(),"usr":TTO.name,"pid":pid,"t":TTO.team,"playsofar":PlaySoFar,"c":(c+1)%6,"room":r }
                            self.askCard(message,TTO)


    def   startNextMatch(self,r):
          RR=self.TrumpObjects[r].rules
          TT=self.TrumpObjects[r].tt
          TT.setNextGame()
          TT.getOrderOfPlayers()
          self.TrumpObjects[r].doTheDeal()
          self.sendCard(self.TrumpObjects[r])
          quNO="R"+str(r)+str(0)
          message={"event":"question","question":"what is your trump?","usr":TT.orderofPlay[0].name,"t":TT.orderofPlay[0].team,"quNo":quNO,"c":0,"room":r}
          self.askQustion(message,self.TrumpObjects[r].tt.orderofPlay[0])





    def didHeWon(self,rules,tt):
                                t0P=rules.getPoints(rules.t0Pidi)
                                t1P=rules.getPoints(rules.t1Pidi)
                                print ('Team0  ' +  str (t0P))
                                print ('Team1  ' +  str (t1P))
                                if rules.t1GetPoint:
                                    if rules.villi <=t1P:
                                        dialoge=("Team1 won  Villichu Jayichu so Just one base")
                                        tt.t1base=tt.t1base+1
                                        tt.t0base=tt.t0base-1
                                        message={"won":"Team1","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message,tt.orderofPlay)
                                        return True
                                    if (56-rules.villi) <=t0P:
                                        dialoge= ("Team0 won by Defending---- Give me two base")
                                        tt.t1base=tt.t1base-2
                                        tt.t0base=tt.t0base+2
                                        message={"won":"Team0","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message,tt.orderofPlay)
                                        return True
                                else:
                                    if rules.villi <=t0P:
                                        dialoge= ("Team0 won Villichu Jayichu so Just one base ")
                                        tt.t0base=tt.t0base+1
                                        tt.t1base=tt.t1base-1
                                        message={"won":"Team0","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message,tt.orderofPlay)
                                        return True
                                    if (56-rules.villi) <=t1P:
                                        dialoge= ("Team1 won by Defending---- Give me two base")
                                        tt.t1base=tt.t1base+2
                                        tt.t0base=tt.t0base-2
                                        message={"won":"Team1","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message,tt.orderofPlay)
                                        return True
                                return False






    def manageVilli(self,AnsNo):
                                      lastVilli=self.getAnswerOfOldquestion(AnsNo)
                                      r=lastVilli["room"]
                                      gamers=self.USERS.listOfRooms[r]
                                      RR=self.TrumpObjects[r].rules
                                      TT=self.TrumpObjects[r].tt
                                      c=lastVilli["c"]
                                      self.boradCast(TT.orderofPlay[c].name + "  called   " + lastVilli["ans"],gamers)

                                      if lastVilli["ans"] == "P":
                                           if len (RR.skipped) ==6:  ## Need to change for 6
                                                  print (RR.villi)
                                                  self.TrumpIsSet({"villi":str (RR.villi),"trump":RR.trump,"dude":RR.dude,"dudeTeam":RR.Dudeteam},TT.orderofPlay)
                                                  if RR.Dudeteam=="Team1":
                                                      RR.t1GetPoint=True
                                                  else:
                                                      RR.t1GetPoint=False
                                                  pid="R"+str(r)+str(1)
                                                  self.sendCard(self.TrumpObjects[r])
                                                  message={"event":"play","hand":TT.orderofPlay[0].showHand(),"usr":TT.orderofPlay[0].name,"pid":pid,"t":"Team0","playsofar":[],"c":0,"room":r }
                                                  self.askCard(message,TT.orderofPlay[0])
                                                  return True
                                           else:
                                                RR.skipped.add(lastVilli["usr"])

                                      else:

                                          RR.villi=int (lastVilli["ans"][1:])
                                          RR.trump=lastVilli["ans"][0]
                                          RR.dude=lastVilli["usr"]
                                          RR.Dudeteam=lastVilli["t"]
                                      quNo=lastVilli["quNo"][:2]+ str (int (lastVilli["quNo"][2:]) +1)
                                      TTO=TT.orderofPlay[(c+1)%6]
                                      message={"event":"question","question":"what is your trump?","usr":TTO.name,"t":TTO.team,"quNo":quNo,"c":(c+1)%6,"room":r}
                                      self.askQustion(message,TTO)

    def TrumpIsSet(self,message,gamers):                            ## This will change as per Room Logic

                   payload = json.dumps({"event":"TrumpIsSet","villi":message["villi"],"trump":message["trump"],"dude":message["dude"],"dudeTeam":message["dudeTeam"]}).encode('utf8')
                   for c in gamers:
                                                                if c.websocket:
                                                                   self.mySendMessage(c.websocket,payload)


    def MatchIsDone(self,message,gamers):
        payload = json.dumps({"event":"MatchIsDone","won":message["won"],"base0":message["base0"],"base1":message["base1"],"dialoge":message["dialoge"]}).encode('utf8')
        for c in gamers:
                                                     if c.websocket:
                                                        self.mySendMessage(c.websocket,payload)
