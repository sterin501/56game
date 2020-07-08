var webSocket;
var user;

jQuery(document).ready(function ($) {
  var contents = '';
  user = document.cookie.split('=')[1];
  if (document.cookie.startsWith("id=")) {
    console.log("id found .. it will create web sorcket ")
    webSocket = new WebSocket("ws://" + window.location.hostname + ":6789/lobby?" + document.cookie);
  }

  webSocket.onmessage = function (message) {
    console.log(message);
    let data = JSON.parse(message.data);

    if (data.event == "lobbyList") {

      console.log("got room details");
      console.log(data.roomDetails);
      if (data.roomDetails) {
        var roomArray = Object.keys(data.roomDetails);

        roomArray.forEach((roomNo, i) => {
          var seatArr = data.roomDetails[roomNo];
          contents += '<div style="color:white">' + roomNo;
          for (var j = 1; j <= 6; j++) {
            contents += '<button type="button" class="btn btn-primary" onclick="goToSeat(' + (i+1) + ',' + j + ')\">' + j + '</button>';
          }
          contents += ' </div>';

        });
        $("#seatSelection")[0].innerHTML = contents;

      }
    }

  } 

});

function goToSeat(roomNo, seatNo) {
  document.location.href = document.location.href.replace("lobby", "table") + "?user=" + user + '&roomNo='
    + roomNo + '&seatNo=' + seatNo;
}
