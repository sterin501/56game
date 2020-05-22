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

TrumpHandler.py -->Object to deal with game and socket 

**bot/bot.py** --

 Atleast one browser to test the game . All bots are set play "P" all calls and play random cards (with in game logic )

it controlls two events 
 
 
1.  "event":"question" -->Requesting trump details from one player 
 
 Request : 
 
 {'event': 'question', 'question': 'what is your trump?', 'usr': 'P___bot3', 't': 'Team0', 'quNo': 3, 'c': 2}

Responce :
{"AnsNo": 3, "Answer": "P", "usr": "P___bot3", "t": "Team0"}

2. 'event': 'play' --> Requesting card from one player 
   Request : 
{'event': 'play', 'hand': ['C9', 'CK', 'D9', 'DK', 'HK', 'SJ', 'SK', 'ST'], 'usr': 'P___bot1', 'pid': 1, 't': 'Team0', 'playsofar': [], 'c': 0}

   Responce :
{"pid":6,"card":"DJ","usr":"P___chrome","t":"Team1","c":5} 

**js/test.html**

it contains javascript to contorl similar bot logic 
it need to keep on http doc root 

1. Need to set key to understand by server 
   http://localhost/test.html?SetKey=chromeORwhatever
 
 2. new WebSocket("ws://127.0.0.1:6789/"+document.cookie) , creating websocket 
 
 *Atleast one browser to test the game . All bots are set play "P" all calls and play random cards (with in game logic )*

 
 
