#!/bin/python3


class Gamer(object):
    def __init__(self, userID, key, websocket, room, seatNo):
        self.userID = userID
        self.key = key
        self.websocket = websocket
        self.TrumpObject = ""
        self.room = room
        self.seatNo = seatNo  ### This seat same for UI . But for array in gamers list ,less than 1 .

    def check(self):
        pass


class UserList(object):
    def __init__(self):
        self.UL = []
        self.keys = []
        self.ws = []  ## Contins only active connection
        self.listOfRooms = []
        for kk in range(0, 5):
            inner = []
            for cc in range(0, 6):
                inner.append(None)
            self.listOfRooms.append(inner)

        # self.listOfRooms=[[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None],[None,None,None,None,None,None]]  # len ([[]])  ---> 1 : 5 rooms created

    def getUserBywebSocket(self, websocket):
        for kk in self.UL:
            if kk.websocket == websocket:
                return (kk)
        return False

    def addtoList(self, gamer):
        self.UL.append(gamer)
        self.keys.append(gamer.key)
        self.ws.append(gamer.websocket)

        print(repr(gamer) + "  is added to list")

    def removeFromRoom(self, ws):
        try:
            print(ws)
            print(self.ws)
            self.ws.remove(ws)
            print("removef from list of ws[]")
            roomNO = -6
            seatNo = -6
            for kk in self.UL:
                print(kk.seatNo)
            for kk in self.UL:
                if (kk.websocket == ws):
                    roomNO = kk.room
                    seatNo = kk.seatNo
                    break
            roomObject = self.listOfRooms[roomNO]
            roomObject[seatNo] = None
            return True
        except Exception as ex:
            print(ex)
            print("Error in Removing the user from room")
            return False

    def getKeyBySocket(self, ws):
        for kk in self.UL:
            if kk.websocket == ws:
                return (kk.key)
        return False

    def checkForkey(self, key):  ## will replace with sqllite
        # print (key +"  checking ")
        if key in self.keys:
            for kk in self.UL:
                print(kk)
                if kk.key == key:
                    return (kk)
        else:
            return False

    def addGameroRomm(self, roomNO, seatNo, player):
        try:
            room = self.listOfRooms[roomNO]
            room[seatNo] = (player)
            return player
        except Exception as ex:
            print(ex)
            print("Rooom add ")

    def canEnterTheRoom(self, roomNO, seatNo):
        if seatNo > 6:
            print("Invalid seat no")
            return False

        if roomNO > 4:  ## Max rooom ,
            print("invalid room")
            return False
        # if  len (self.listOfRooms[roomNO]) < 6:   #kk.append(user)
        roomObject = self.listOfRooms[roomNO]
        if roomObject[seatNo] is None:
            print("Will add in room ")
            return True
        else:
            print("Seat is occupied")
            return False

    def getRoomDetails(self, websocket):
        # room=0
        for kk in self.UL:
            if kk.websocket == websocket:
                print(kk.room)
                print(self.listOfRooms)
                return ({"room": kk.room, "gamersInRomm": self.listOfRooms[kk.room]})
        return False

    def getPlayerBywebsocket(self, websocket):
        return self.listOfRooms[room]
