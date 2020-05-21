#!/bin/python
import kuthu
import Player
import random
import RuleBook
import table





def makeMove(ThePlayer,IsValid,currentCard,thisPlay):
    #print ("Begining  " + currentCard)
    if not IsValid:
      if ThePlayer.bot:
        currentCard=random.choice(ThePlayer.hand)
      else:
        sel = int ( input("Enter Choice  0-" + str (  len (ThePlayer.hand) -1) + "   ?  "))
        if sel < len (ThePlayer.hand):
          currentCard = ThePlayer.hand[sel]
        else:
            print ("Invalid Choice ")
            currentCard=makeMove(ThePlayer,False,currentCard,thisPlay)

      if validMove(ThePlayer,currentCard,thisPlay):
          currentCard=makeMove(ThePlayer,True,currentCard,thisPlay)
          print ( ("Playing  " + ThePlayer.name + "    -->  " + displayNice(currentCard)))
          ThePlayer.removeCard(currentCard)
          return (currentCard)

      else:
           currentCard=makeMove(ThePlayer,False,currentCard,thisPlay)

    return (currentCard)




def validMove(ThePlayer,cardToCheck,thisPlay):
    if ( len (thisPlay) == 0):
            return True
    else:
        currentSign=thisPlay[0][0]
        for kk in ThePlayer.hand:
            if kk[0] == currentSign:
                 if cardToCheck[0] == currentSign:
                     return True
                 else:
                     #print ("You have that sign . Please enter it ")
                     return False
    return True

def whoGotit(thisPlay,rules,tt):
    if rules.IsTrumpInPlay(thisPlay):
        print ("Trump Round")
        C=rules.trumpInAction(thisPlay)
    else:
        C=rules.whoIsLeader(thisPlay)

    team=tt.orderofPlay[C].team
    print (C)
    print (team)
    if team == "Team0":
         rules.t0Pidi.append(thisPlay)
    else:
         rules.t1Pidi.append(thisPlay)
    tt.opener=C
    tt.getOrderOfPlayers()






def displayNice(chittu):
    #print (chittu)
    #print (type(chittu))
    if chittu[0] == ("S"):
        return (u"\u2660 "+chittu[1])
    elif chittu[0] == ("C"):
        return (u"\u2663 "+chittu[1])
    elif chittu[0] == ("H"):
        return (u"\u2665\uFE0F  "+chittu[1])
    elif chittu[0] == ("D"):
        return (u"\u2666\uFE0F  "+chittu[1])

def setThurpu(tt,rules):
    print ('Set Trump Card please')
    c=0
    while len (rules.skipped) < 6:

           if not tt.orderofPlay[c].name in rules.skipped:
              settingTrump(tt.orderofPlay[c],rules)
           c=c+1
           if c == 6:
               c = 0

    if rules.Dudeteam=="Team1":

        rules.t1GetPoint=True
        print ("Team1  ___ Dude  " + rules.dude)
        print ("Villi " + str (rules.villi) )
    else:

        rules.t1GetPoint=False
        print ("Team0 _____ Dude  " + rules.dude)
        print ("Villi " + str (rules.villi) )



def  settingTrump(Player,rules):
     print ("Player  "+ Player.name)
     if Player.bot:
         ch=random.choice([True,False])
         if ch:
            rules.villi=rules.villi+1
            rules.trump=random.choice(["C","H","S","D"])
            rules.dude=Player.name
            rules.Dudeteam=Player.team
         else:
            rules.skipped.append(Player.name)
     else:
        need =   raw_input("Do you call (y/n)?")
        print (need)
        if need == "y":
          rules.villi=rules.villi+1
          rules.trump=raw_input("Enter Trump Sign (S,D,H,C)? ")
          rules.dude=Player.name
          rules.Dudeteam=Player.team
        else:
           rules.skipped.append(Player.name)
     print ("Villi now " + str (rules.villi) )

def doTheDeal(P1,P2,P3,P4,P5,P6):
    ss=kuthu.Card()
    P1.hand=ss.p1
    P2.hand=ss.p2
    P3.hand=ss.p3
    P4.hand=ss.p4
    P5.hand=ss.p5
    P6.hand=ss.p6

def didHeWon(rules,tt):
    t0P=rules.getPoints(rules.t0Pidi)
    t1P=rules.getPoints(rules.t1Pidi)
    print ('Team0  ' +  str (t0P))
    print ('Team1  ' +  str (t1P))
    if rules.t1GetPoint:
        if rules.villi <=t1P:
            print ("Team1 won  Villichu Jayichu so Just one base")
            tt.t1base=tt.t1base+1
            tt.t0base=tt.t0base-1
            return True
        if (56-rules.villi) <=t0P:
            print ("Team0 won by Defending---- Give me two base")
            tt.t1base=tt.t1base-2
            tt.t0base=tt.t0base+2
            return True
    else:
        if rules.villi <=t0P:
            print ("Team0 won Villichu Jayichu so Just one base ")
            tt.t0base=tt.t0base+1
            tt.t1base=tt.t1base-1
            return True
        if (56-rules.villi) <=t1P:
            print ("Team1 won by Defending---- Give me two base")
            tt.t1base=tt.t1base+2
            tt.t0base=tt.t0base-2
            return True
    return False


if __name__ == "__main__":
    P1=Player.Player("p1","Team0",True)
    P2=Player.Player("p2","Team1",True)
    P3=Player.Player("p3","Team0",True)
    P4=Player.Player("p4","Team1",True)
    P5=Player.Player("p5","Team0",True)
    P6=Player.Player("p6","Team1",False)
    tt = table.Table(P1,P2,P3,P4,P5,P6)
    P1.sayHello()
    P6.sayHello()
    print ("Starting Table in Califorina")

    while True:

        print ("Game " + str (tt.gameCount))
        print (" Lets start maggie")
        print ("Make the deal______________________________________")
        doTheDeal(tt.P1,tt.P2,tt.P3,tt.P4,tt.P5,tt.P6)
        tt.P6.showHand()
        tt.P6.showHandinUTF()
        #FristKalli=tt.getOrderOfPlayers()
        tt.getOrderOfPlayers()

        print ("Frist player (Kallikaran )  is  "+ tt.orderofPlay[0].name)

        rules=RuleBook.Points()

        setThurpu(tt,rules)
        print ("______________________________________\n\n")
        print ("Team1  " if rules.t1GetPoint else "Team0   ")
        print (rules.dude + " Called   " + str (rules.villi)  +"  "+ rules.trump)
        print ("______________________________________\n\n")

        for kk in range(1,9):
           print ("Round    " + str (kk))
           tt.P6.showHandinUTF()
           thisPlay=[]
           for cc in range(0,6):
                thisPlay.append(makeMove(tt.orderofPlay[cc],False,"",thisPlay))
           print (thisPlay)
           whoGotit(thisPlay,rules,tt)
           if  didHeWon(rules,tt):
               break
           #tt.P6.showHandinUTF()

        print (rules.t0Pidi)
        print (rules.t1Pidi)
        print ("################################")
        print ("Base now:: Team0  "+ str (tt.t0base)  + "    Team1   " + str (tt.t1base))
        print ("################################")
        tt.setNextGame()
