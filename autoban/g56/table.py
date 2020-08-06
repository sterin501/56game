#!/bin/python


class Table(object):
    def __init__(self, p1, p2, p3, p4, p5, p6):
        self.P1 = p1
        self.P2 = p2
        self.P3 = p3
        self.P4 = p4
        self.P5 = p5
        self.P6 = p6
        self.t0base = 5
        self.t1base = 5
        self.gameCount = 1
        self.opener = 0
        self.orderofPlay = [self.P1, self.P2, self.P3, self.P4, self.P5, self.P6]
        self.listOfKunugu = []
        self.KunugSetAt=-1
        self.lastKunugTeam=""



    def getPlayerName(self,P):
        #print ( self.__dict__[P].name)
        return (self.__dict__[P].name)

    def setNextGame(self):
        self.gameCount = self.gameCount + 1
        self.opener = (self.gameCount - 1) % 6
        self.orderofPlay = [self.P1, self.P2, self.P3, self.P4, self.P5, self.P6]

    def t1VillichuWon(self, villi, seatNo):
        if villi == 56:
            self.t1base = self.t1base + 3
            self.t0base = self.t0base - 3
        elif villi > 39:
            self.t1base = self.t1base + 2
            self.t0base = self.t0base - 2
        else:
            self.t1base = self.t1base + 1
            self.t0base = self.t0base - 1

        if self.KunugSetAt+1==self.gameCount and self.lastKunugTeam=="team1":
            print ("Used in first chance Team1, so removing all ")
            self.listOfKunugu.remove(self.P2.seatNo)
            self.listOfKunugu.remove(self.P4.seatNo)
            self.listOfKunugu.remove(self.P6.seatNo)
            return True


        self.checkForKunuk()
        if seatNo in self.listOfKunugu:
            self.listOfKunugu.remove(seatNo)

    def t1VillichuLoss(self, villi):
        if villi == 56:
            self.t1base = self.t1base - 4
            self.t0base = self.t0base + 4
        elif villi > 39:
            self.t1base = self.t1base - 3
            self.t0base = self.t0base + 3
        else:
            self.t1base = self.t1base - 2
            self.t0base = self.t0base + 2
        self.checkForKunuk()

    def t0VillichuWon(self, villi, seatNo):
        if villi == 56:
            self.t1base = self.t1base - 3
            self.t0base = self.t0base + 3
        elif villi > 39:
            self.t1base = self.t1base - 2
            self.t0base = self.t0base + 2
        else:
            self.t1base = self.t1base - 1
            self.t0base = self.t0base + 1

        if self.KunugSetAt+1==self.gameCount  and self.lastKunugTeam=="team0":
                print ("Used in first chance Team0, so removing all ")
                self.listOfKunugu.remove(self.P1.seatNo)
                self.listOfKunugu.remove(self.P3.seatNo)
                self.listOfKunugu.remove(self.P5.seatNo)
                return True


        self.checkForKunuk()
        if seatNo in self.listOfKunugu:
            self.listOfKunugu.remove(seatNo)

    def t0VillichuLoss(self, villi):
        if villi == 56:
            self.t1base = self.t1base + 4
            self.t0base = self.t0base - 4
        elif villi > 39:
            self.t1base = self.t1base + 3
            self.t0base = self.t0base - 3
        else:
            self.t1base = self.t1base + 2
            self.t0base = self.t0base - 2
        self.checkForKunuk()

    def checkForKunuk(self):
        if self.t1base < 0:
            print("kunugu for team1 ")
            print(self.gameCount)
            self.t1base = 5
            self.t0base = 5
            self.KunugSetAt=self.gameCount
            self.listOfKunugu.append(self.P2.seatNo)
            self.listOfKunugu.append(self.P4.seatNo)
            self.listOfKunugu.append(self.P6.seatNo)
            self.lastKunugTeam="team1"
            return True
        if self.t0base < 0:
            print("kunugu for team0 ")
            print(self.gameCount)
            self.t1base = 5
            self.t0base = 5
            self.KunugSetAt=self.gameCount
            self.listOfKunugu.append(self.P1.seatNo)
            self.listOfKunugu.append(self.P3.seatNo)
            self.listOfKunugu.append(self.P5.seatNo)
            self.lastKunugTeam="team0"
            return True
        return False

    def getOrderOfPlayers(self):
        # print ("opener     --->" + str (self.opener))
        temp = []
        if self.opener == 0:
            print('')
        elif self.opener == 1:
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            self.orderofPlay = temp

        elif self.opener == 2:
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            self.orderofPlay = temp

        elif self.opener == 3:
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            self.orderofPlay = temp
        elif self.opener == 4:
            temp.append(self.orderofPlay[4])
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            self.orderofPlay = temp
        elif self.opener == 5:
            temp.append(self.orderofPlay[5])
            temp.append(self.orderofPlay[0])
            temp.append(self.orderofPlay[1])
            temp.append(self.orderofPlay[2])
            temp.append(self.orderofPlay[3])
            temp.append(self.orderofPlay[4])
            self.orderofPlay = temp
