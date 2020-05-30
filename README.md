# 56game

 **server.py**   --> Used to start the server 

class ChatProtocol :

OnConnect() produces websocket object.

onMessage() redirect to MangeMeasage class based on responce from client 

 {"AnsNo":4,"Answer":"P","usr":"P1","t":"Team0"}'  -- For setting Trump  Responce 
 
 
 {"pid":pid,"card":data.value,"usr":obj.usr,"t":obj.t} -- For Cards Play 
 
 
 
 
**manageMessage.py** --> Control object from server.py and Send to TrumpHandler Object 
 
 All the messages are controlled using listOfQ,listOfC list
 
 status = "DONE" when get responce from clien t
 
 
 **Events**:
 
 "event":"broadcast" --> Sending info to all clients in room     
 
 
 
 "event":"cardSend" --> Sending cards  to specific user   
 
 
 "event":"question" -->Requesting trump details from one player   
 
 "event":"TrumpIsSet" --> Sending trump details to all users in room 
 
 "event":"cardPlay" --> Sending cards during play in room 
 
 "event":"play"   ---> Requesting card from one player 
 
 "event":"MatchIsDone" --> Sending end of Match details to users in room
 
 "event":"Reconnect" --> When user reconnets to the game 
 
 Example ::
 
 {'event': 'Reconnect', 'villi': '28', 'trump': 'S', 'dude': 'P1', 'dudeTeam': 'Team0', 'hand': ['CA', 'CJ', 'CQ', 'CQ', 'DA', 'H9', 'HT', 'S9'], 'VSF': ['P', 'P', 'P', 'P', 'P', 'P'], 'playsofar': ['SQ']}
 
 {'event': 'MatchIsDone', 'won': 'Team1', 'base0': 3, 'base1': 7, 'dialoge': 'Team1 won by Defending---- Give me two base', 'Mc': 1}

{'event': 'TrumpIsSet', 'villi': '28', 'trump': 'S', 'dude': 'P1', 'dudeTeam': 'Team0'}



TrumpHandler.py -->Object to deal with game and socket 

**bot/bot.py** --

 Atleast one browser to test the game . All bots are set play "P" all calls and play random cards (with in game logic )

it controlls two events 
 
 
1.  "event":"question" -->Requesting trump details from one player 
 
 Request : 

{'event': 'question', 'question': 'what is your trump?', 'usr': 'P___bot6', 't': 'Team1', 'quNo': 'R05', 'c': 5, 'r': 0, 'SN': 6, 'VSF': ['P', 'P', 'P', 'P', 'P']}


Responce :
'{"AnsNo": "R00", "Answer": "P", "usr": "P___bot1", "t": "Team0"}'


2. 'event': 'play' --> Requesting card from one player 
   Request : 
{'event': 'play', 'hand': ['C9', 'CK', 'CQ', 'DJ', 'HJ', 'HJ', 'HQ', 'SK'], 'usr': 'P___bot6', 'pid': 'R06', 't': 'Team1', 'playsofar': ['SA', 'SJ', 'SQ', 'S9', 'SA'], 'c': 5, 'r': 0, 'SN': 6}


   Responce :
{"pid": "R06", "card": "SK", "usr": "P___bot6", "t": "Team1"}'


**js/test.html**

it contains javascript to contorl similar bot logic 
it need to keep on http doc root 

1. Need to set key to understand by server 
   http://localhost/test.html?SetKey=chromeORwhatever
 
 2. new WebSocket("ws://127.0.0.1:6789/"+document.cookie+"&Room=0&seatNo=2") , creating websocket 
 
 websocket connection should this order key m  Room and SeatNo
 
 *Atleast one browser to test the game . All bots are set play "P" all calls and play random cards (with in game logic )*

 
_________________________________________________________________________________________________

**Testing**

1. Install python lib : 
 pip3 install asyncio autobahn
 
2. start server using
./server.py

3. start bot using 
 ./bot.py  "ws://127.0.0.1:6789/key=bot1&Room=0&seatN0=6"

 default room is 0
4. Install webserver 
 
5. Copy js/test.html to webserver httpRoot directory

6. Set Key to name the browser session
http://localhost/test.html?SetKey=chromeORwhatever
 
 
 
