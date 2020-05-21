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
        self.TrumpObjects=[]

    def register(self,websocket,key):

                user=self.USERS.checkForkey(key)
                #print (user)
                if   user:
                     #print (user)
                     print ("user already in table")
                     if websocket in self.USERS.ws:
                         print ("ok ")
                     else:
                         print ("we will re assign ")
                         user.websocket=websocket
                         #self.boradCast("Reconnected "+username)


                else:
                    #print (" adding to list")
                    username=("P"+ "___"+key )  ##  This will change to sqllite Actitivy in USerList Object  ## str( random.randint(9,7568)
                    gamerObject=Gamer(username,key,websocket)
                    self.USERS.addtoList(gamerObject)
                    #self.boradCast("New user joined "+username)





    def  boradCast(self,message):                            ## This will change as per Room Logic

                         payload = json.dumps({"event":"broadcast","message":message}).encode('utf8')
                         for c in self.USERS.UL:
                              if c.websocket:
                                 c.websocket.sendMessage(payload, False)



    def playSoFar(self,message):                            ## This will change as per Room Logic

                         payload = json.dumps({"event":"cardPlay","message":message["msg"],"playsofar":message["playsofar"]}).encode('utf8')
                         for c in self.USERS.UL:
                              if c.websocket:
                                 c.websocket.sendMessage(payload, False)

    def  sendCard(self,th):                            ## This will change as per Room Logic
                         #payload = json.dumps({"event":"broadcast","message":message}).encode('utf8')
                          for kk in   th.tt.orderofPlay:
                                   if kk.websocket:
                                      payload = json.dumps({"event":"cardSend","hand":kk.hand}).encode('utf8')
                                      #payload = json.dumps({"event":"cardSend","cards":kk.showHandinUTF()}).encode('utf8')
                                      kk.websocket.sendMessage(payload, False)



    def askQustion(self,message,client):
                            payload = json.dumps(message).encode('utf8')
                            client.websocket.sendMessage(payload,False)
                            self.listOfQ.append({"quNo":message["quNo"],"status":"Asked","ans":"","usr":message["usr"],"t":message["t"],"c":message["c"]})
                            print ("Question1 Asked")

    def askCard(self,message,client):
                            payload = json.dumps(message).encode('utf8')
                            client.websocket.sendMessage(payload,False)
                            self.listOfC.append({"pid":message["pid"],"status":"Asked","card":"","usr":message["usr"],"t":message["t"],"c":message["c"]})
                            print ("Card  Asked")

    def canWeStart(self):

                                  if len (self.USERS.UL) ==6:  ## Need to change to Room logic .
                                      #self.USERS.creatBotPlayers()
                                      th=TrumpHandler.TrumpHandler(self.USERS.UL)
                                      st=th.publicTextBeforeEveryMatch()+"  ....   ....  "
                                      th.doTheDeal()
                                      th.tt.getOrderOfPlayers()
                                      self.TrumpObjects.append(th)
                                      self.boradCast ({"event":"broadcast","message":st})
                                      self.sendCard(th)
                                      message={"event":"question","question":"what is your trump?","usr":"P1","t":"Team0","quNo":1,"c":0}
                                      self.askQustion(message,self.TrumpObjects[0].tt.orderofPlay[0])

                                  else:
                                      self.boradCast ("you need to wait")


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
                            RR=self.TrumpObjects[0].rules
                            TT=self.TrumpObjects[0].tt
                            self.TrumpObjects[0].thisPlay.append(lastCard["card"])
                            PlaySoFar=self.TrumpObjects[0].thisPlay
                            c=lastCard["c"]                  ## --> Order of Index
                            TT.orderofPlay[c].removeCard(lastCard["card"])
                            self.playSoFar({"msg":TT.orderofPlay[c].name+ "  played  "+ lastCard['card'], "playsofar":PlaySoFar})
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
                                self.TrumpObjects[0].thisPlay=[]
                                if team == "Team0":
                                             RR.t0Pidi.append(PlaySoFar)
                                else:
                                             RR.t1Pidi.append(PlaySoFar)
                                TT.opener=newC
                                TT.getOrderOfPlayers()
                                PlaySoFar=[]  ### To prevent 6 cards in second play
                                if self.didHeWon(RR,TT):
                                    print ("won")
                                    self.startNextMatch()
                                    return True



                            TTO=TT.orderofPlay[(c+1)%6]
                            message={"event":"play","hand":TTO.showHand(),"usr":TTO.name,"pid":lastCard["pid"]+1,"t":TTO.team,"playsofar":PlaySoFar,"c":(c+1)%6 }
                            self.askCard(message,TTO)


    def   startNextMatch(self):
          RR=self.TrumpObjects[0].rules
          TT=self.TrumpObjects[0].tt
          TT.setNextGame()
          TT.getOrderOfPlayers()
          self.TrumpObjects[0].doTheDeal()
          self.sendCard(self.TrumpObjects[0])
          message={"event":"question","question":"what is your trump?","usr":TT.orderofPlay[0].name,"t":TT.orderofPlay[0].team,"quNo":1,"c":0}
          self.askQustion(message,self.TrumpObjects[0].tt.orderofPlay[0])





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
                                        self.MatchIsDone(message)
                                        return True
                                    if (56-rules.villi) <=t0P:
                                        dialoge= ("Team0 won by Defending---- Give me two base")
                                        tt.t1base=tt.t1base-2
                                        tt.t0base=tt.t0base+2
                                        message={"won":"Team0","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message)
                                        return True
                                else:
                                    if rules.villi <=t0P:
                                        dialoge= ("Team0 won Villichu Jayichu so Just one base ")
                                        tt.t0base=tt.t0base+1
                                        tt.t1base=tt.t1base-1
                                        message={"won":"Team0","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message)
                                        return True
                                    if (56-rules.villi) <=t1P:
                                        dialoge= ("Team1 won by Defending---- Give me two base")
                                        tt.t1base=tt.t1base+2
                                        tt.t0base=tt.t0base-2
                                        message={"won":"Team1","base0":tt.t0base,"base1":tt.t1base,"dialoge":dialoge}
                                        self.MatchIsDone(message)
                                        return True
                                return False






    def manageVilli(self,AnsNo):
                                      lastVilli=self.getAnswerOfOldquestion(AnsNo)
                                      RR=self.TrumpObjects[0].rules
                                      TT=self.TrumpObjects[0].tt
                                      c=lastVilli["c"]
                                      self.boradCast(TT.orderofPlay[c].name + "  called   " + lastVilli["ans"])

                                      if lastVilli["ans"] == "P":
                                           if len (RR.skipped) ==6:  ## Need to change for 6
                                                  print (RR.villi)
                                                  self.TrumpIsSet({"villi":str (RR.villi),"trump":RR.trump,"dude":RR.dude,"dudeTeam":RR.Dudeteam})
                                                  if RR.Dudeteam=="Team1":
                                                      RR.t1GetPoint=True
                                                  else:
                                                      RR.t1GetPoint=False

                                                  self.sendCard(self.TrumpObjects[0])
                                                  message={"event":"play","hand":TT.orderofPlay[0].showHand(),"usr":TT.orderofPlay[0].name,"pid":1,"t":"Team0","playsofar":[],"c":0 }
                                                  self.askCard(message,TT.orderofPlay[0])
                                                  return True
                                           else:
                                                RR.skipped.add(lastVilli["usr"])

                                      else:

                                          RR.villi=int (lastVilli["ans"][1:])
                                          RR.trump=lastVilli["ans"][0]
                                          RR.dude=lastVilli["usr"]
                                          RR.Dudeteam=lastVilli["t"]

                                      TTO=TT.orderofPlay[(c+1)%6]
                                      message={"event":"question","question":"what is your trump?","usr":TTO.name,"t":TTO.team,"quNo":lastVilli['quNo']+1,"c":(c+1)%6}
                                      self.askQustion(message,TTO)

    def TrumpIsSet(self,message):                            ## This will change as per Room Logic

                   payload = json.dumps({"event":"TrumpIsSet","villi":message["villi"],"trump":message["trump"],"dude":message["dude"],"dudeTeam":message["dudeTeam"]}).encode('utf8')
                   for c in self.USERS.UL:
                                                                if c.websocket:
                                                                   c.websocket.sendMessage(payload, False)


    def MatchIsDone(self,message):
        payload = json.dumps({"event":"MatchIsDone","won":message["won"],"base0":message["base0"],"base1":message["base1"],"dialoge":message["dialoge"]}).encode('utf8')
        for c in self.USERS.UL:
                                                     if c.websocket:
                                                        c.websocket.sendMessage(payload, False)
