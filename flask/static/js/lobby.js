  var webSocket;
  var user;

    jQuery(document).ready(function ($) {

            console.log(document.cookie);
            if (document.cookie.startsWith("id="))
            {
              console.log("id found .. it will create web sorcket ")
              webSocket = new WebSocket("ws://" + window.location.hostname + ":6789/lobby?" + document.cookie);
            }

            webSocket.onmessage = function (message) {
                console.log(message);
                let data = JSON.parse(message.data);

                if (data.event == "lobbyList"){

                  console.log("got room details");
                  console.log(data.roomDetails);
                }

              } // end of on message


    });
