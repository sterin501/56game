#!/bin/python




class Table(object):
    def __init__(self, p1,p2,p3,p4,p5,p6):
        self.P1=p1
        self.P2=p2
        self.P3=p3
        self.P4=p4
        self.P5=p5
        self.P6=p6
        self.t0base=5
        self.t1base=5
        self.gameCount=1
        self.opener=0
        self.orderofPlay=[self.P1,self.P2,self.P3,self.P4,self.P5,self.P6]
    def setNextGame(self):
            self.gameCount=self.gameCount+1
            self.opener=(self.gameCount-1)%6
            self.orderofPlay=[self.P1,self.P2,self.P3,self.P4,self.P5,self.P6]

    def getOrderOfPlayers(self):
        #print ("opener     --->" + str (self.opener))
        temp=[]
        if self.opener==0:
             print('')
        elif self.opener==1:
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            self.orderofPlay=temp

        elif self.opener==2:
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            self.orderofPlay=temp

        elif self.opener==3:
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            self.orderofPlay=temp
        elif self.opener==4:
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            self.orderofPlay=temp
        elif self.opener==5:
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            self.orderofPlay=temp
