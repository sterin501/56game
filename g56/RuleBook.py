#!/bin/python

## Rule for 28 Game

class Points(object):

   def __init__(self):
       #J=3
       #Nine=2
       #A=1
       #T=1
       #Team1=["P1","P3"]
       #Team2=["P2","P4"]
       self.villi=28
       self.VSF=[]       ## villi so far 
       self.trump="S"
       self.t0Pidi=[]
       self.t1Pidi=[]
       self.dude="P1"
       self.skipped=set()
       self.orderOfCard=["7","8","Q","K","T","A","9","J"]
       self.t1GetPoint=True
       self.Dudeteam="Team0"

   def whoIsLeader(self,thisPlay):
       FS=thisPlay[0][0]
       leaderC=0
       indexBefore=-1
       c=0
       for kk in thisPlay:
           if FS in kk:
               indexC=self.orderOfCard.index(kk[1])
               #print (indexC)
               if indexC > indexBefore:
                  leaderC=c
                  indexBefore=indexC
           c=c+1
       return (leaderC)

   def trumpInAction(self,thisPlay):
       leaderC=0
       indexBefore=-1
       c=0
       for kk in thisPlay:
           if self.trump in kk:
               indexC=self.orderOfCard.index(kk[1])
               #print ("trmp at  " + str (indexC))
               #print ("c  -->" + str (c))
               if indexC > indexBefore:
                  leaderC=c
                  indexBefore=indexC
           c=c+1
       return (leaderC)


   def getPoints(self,pidi):
       point=0
       for outer in pidi:
         for kk in outer:
           if "J" in kk[1]:
               point=point+3
           elif "9" in  kk[1]:
               point=point+2
           elif "T" in  kk[1]:
               point=point+1
           elif "A" in  kk[1]:
               point=point+1
       return (point)

   def IsTrumpInPlay(self,thisPlay):
       for kk in thisPlay:
           if self.trump in kk:
               return True
       return False
