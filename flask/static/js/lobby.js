var webSocket;
var user;
var ghostUser;
var seatNo;
var groomNo;

jQuery(document).ready(function($) {
    var contents = '';
    user = document.cookie.split('=')[1];
    if (document.cookie.startsWith("id=")) {
        console.log("id found .. it will create web sorcket ")
        webSocket = new WebSocket("ws://" + window.location.hostname + ":6789/lobby?" + document.cookie);
    }

    webSocket.onmessage = function(message) {
        console.log(message);
        let data = JSON.parse(message.data);

        if (data.event == "lobbyList") {

          //  console.log("got room details");
          //   console.log(data.roomDetails);
            if (data.roomDetails) {
                var roomArray = Object.keys(data.roomDetails);
                var contents = "";

                roomArray.forEach((roomNo, i) => {
                    var seatArr = data.roomDetails[roomNo];
                  //  console.log(seatArr);
                    contents += '<div style="color:white">' + roomNo;
                    for (var j = 1; j <= 6; j++) {
                        //      console.log(data.roomDetails[roomNo][j-1]);
                        text = data.roomDetails[roomNo][j - 1];

                        if (text == "Empty") {
                            contents += '<button type="button"  class="btn btn-info" onclick="goToSeat(' + (i + 1) + ',' + j + ')\">' + text + '</button>';
                        } else {
                            contents += '<button type="button" disabled  class="btn btn-info" onclick="goToSeat(' + (i + 1) + ',' + j + ')\">' + text + '</button>';
                        }

                    }
                    contents += '<button type="button" class="btn btn-secondary" onclick="goToWatcherSeat(' + (i + 1) + ',' + 1 + ')\">Watch</button>';
                    contents += ' </div>';
                    for (var i = 0; i < seatArr.length; i++) {

                                    if (seatArr[i].equals == user)
                                      {
                                        ghostUser=true;
                                        console.log("ghost user");
                                        seatNo=(i+1);
                                        groomNo=roomNo+1;
                                      }
                    }

                });

                $("#seatSelection")[0].innerHTML = contents;

            }
        }

    }

});

function goToSeat(roomNo, seatNo) {
    document.location.href = document.location.href.replace("lobby", "table") + "?roomNo=" + roomNo + "&seatNo=" + seatNo;
}

function goToWatcherSeat(roomNo, seatNo) {
    document.location.href = document.location.href.replace("lobby", "table") + "?roomNo=" + roomNo + "&seatNo=" + seatNo + "&role=watcher";
}

function goToLobby() {
    document.location.href = document.location.href.replace("home", "lobby");
}

function logout() {
             console.log(webSocket);
             if (ghostUser)
             {
               var resetRequest = {};
               resetRequest.resetID = "RestRequest";
               resetRequest.usr = user;
               resetRequest.r = groomNo;
               resetRequest.SN = seatNo;
               console.log(resetRequest);
              // webSocket.send(JSON.stringify(resetRequest));

             }

             document.location.href = document.location.href.replace("lobby", "logout");
}
