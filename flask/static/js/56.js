var seatNumber;
var webSocket;
var hand;
var uuid = createUUID();
var globalData = {};
var questionData = {};
var playData = {};
var folderButtonStatus = false;
var foldData = {};
var user;
var roomNo;
var seatNo;
var role;
var names;
var toggleAutoPassState = false;
var watchers;
//console.log(uuid);
if (!document.cookie) {
    document.cookie = "key=" + uuid + ";max-age=2592000;"
}
function createUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
function refreshHand(data) {
    var cardsContent = "";
    if (data.hand) {
        $.each(data.hand, function (index, value) {
            cardsContent += "<img id='card1' class='card' src='static/cards/" + value + ".svg' name=" + value + " onclick=selectCard(this)>";
        });
    }
    if (cardsContent) {
        $("#activeHand")[0].innerHTML = cardsContent;
    }

    if (data.villi) {
        let team = 'Red';
        $("#trumpSection")[0].style.color = "red";
        if (data.dudeTeam == 'Team0') {
            team = "Black"
            $("#trumpSection")[0].style.color = "black";
        }
        $("#trumpSection")[0].innerHTML = "Bid : " + team + " " + data.villi + convertToSign(data.trump);
    }

    if (data.playsofar && data.playsofar.length != 0) {
        showOtherCards(data.playsofar);
    }
    if (data.VSF && (!globalData.playsofar || globalData.playsofar.length == 0)) {
        showVili(data.VSF);
    }

    if (data.names) {
        if (data.KunuguSeat) {
            populateNames(kunuguLogic(data.names, data.KunuguSeat));
        }


        else {
            populateNames(data.names);
        }

        if (data.watchlist){              // watch list logic
                    if (JSON.stringify(watchers)!=JSON.stringify(data.watchlist) )
                      {

                      $("#watechers").attr("data-content", data.watchlist);
                      $("#watechers").popover(true, false, "", 3000, false, "left");
                      setTimeout(function () { $("#watechers").popover("hide"); }, 4000);
                      $("#watechers").popover("show");
                      watchers=data.watchlist;
                     }

        }
    }  // end of name check

}

function kunuguLogic(myNames, KunuguSeat) {
    if (typeof KunuguSeat === "undefined") {
        return myNames;
    }

    for (var j = 1; j < 7; j++) {
        myNames["SN" + j] = myNames["SN" + j].replace(/☔/g, "");   // ☔ ,
    }


    for (var i = 0; i < KunuguSeat.length; i++) {
        if (KunuguSeat[i] == 1)
            myNames["SN1"] = myNames["SN1"] + "☔"; // Need to replace with actual kunugu
        else if (KunuguSeat[i] == 2)
            myNames["SN2"] = myNames["SN2"] + "☔";
        else if (KunuguSeat[i] == 3)
            myNames["SN3"] = myNames["SN3"] + "☔";
        else if (KunuguSeat[i] == 4)
            myNames["SN4"] = myNames["SN4"] + "☔";
        else if (KunuguSeat[i] == 5)
            myNames["SN5"] = myNames["SN5"] + "☔";
        else if (KunuguSeat[i] == 6)
            myNames["SN6"] = myNames["SN6"] + "☔";
    }

    return (myNames);
}


function populateNames(names) {
    $('span[name="N1"]')[0].innerHTML = names["SN1"];
    $('span[name="N2"]')[0].innerHTML = names["SN2"];
    $('span[name="N3"]')[0].innerHTML = names["SN3"];
    $('span[name="N4"]')[0].innerHTML = names["SN4"];
    $('span[name="N5"]')[0].innerHTML = names["SN5"];
    $('span[name="N6"]')[0].innerHTML = names["SN6"];
    // backgorund color
    $('span[name="N1"]')[0].style.backgroundColor = "black";
    $('span[name="N2"]')[0].style.backgroundColor = "red";
    $('span[name="N3"]')[0].style.backgroundColor = "black";
    $('span[name="N4"]')[0].style.backgroundColor = "red";
    $('span[name="N5"]')[0].style.backgroundColor = "black";
    $('span[name="N6"]')[0].style.backgroundColor = "red";
    globalData.names = names;


}
function showVili(VSF) {
    if (VSF) {
        resetVSF();
        for (j = VSF.length - 1; j > -1; j--) {
            let seatNo = Object.keys(VSF[j])[0];
            var vili = VSF[j][seatNo];
            let viliToShow;

            if (vili == 'P') {
                viliToShow = 'Pass';
            }
            else {
                viliToShow = convertToSign(vili.substring(0, 1)) + vili.substring(1);
            }

            if (viliToShow == 'undefined') {
                viliToShow = '';
            }
            if (viliToShow.substring(0, 1) == '♥' || viliToShow.substring(0, 1) == '♦') {
                $('span[name="' + seatNo + '"]')[0]
                    .innerHTML = $('span[name="' + seatNo + '"]')[0]
                        .innerHTML + ' ' + '<span class =\"card-text badge badge-light\" style = \"border-radius: 0rem ;background-color: yellow;color:red; padding:0; font-size:100%\">' + viliToShow + '</span>';
            } else if (viliToShow.substring(0, 1) == '♠' || viliToShow.substring(0, 1) == '♣') {
                $('span[name="' + seatNo + '"]')[0]
                    .innerHTML = $('span[name="' + seatNo + '"]')[0]
                        .innerHTML + ' ' + '<span class =\"card-text badge badge-light\" style = \"border-radius: 0rem ;background-color: yellow;color:black; padding:0; font-size:100%\">' + viliToShow + '</span>';
            } else if (viliToShow == 'Pass') {
                $('span[name="' + seatNo + '"]')[0]
                    .innerHTML = $('span[name="' + seatNo + '"]')[0]
                        .innerHTML + ' ' + '<span class =\"card-text badge badge-light\" style = \"border-radius: 0rem ;background-color: yellow;color:black; padding:0; font-size:100%\">' + viliToShow + '</span>';
            }
            else {
                $('span[name="' + seatNo + '"]')[0]
                    .innerHTML = $('span[name="' + seatNo + '"]')[0]
                        .innerHTML + ' ' + '<span class =\"card-text badge badge-light\" style = \"border-radius: 0rem ;background-color: yellow;color:black; padding:0; font-size:100%\">' + viliToShow + '</span>';
            }
        }

    }
}
function resetSpinner() {
    //spinner
    for (var i = 1; i < 7; i++) {
        $('div[name="S' + i + '"]').hide();
    }
}
function resetVSF() {
    $('span[name="S1"]')[0].innerHTML = '';
    $('span[name="S2"]')[0].innerHTML = '';
    $('span[name="S3"]')[0].innerHTML = '';
    $('span[name="S4"]')[0].innerHTML = '';
    $('span[name="S5"]')[0].innerHTML = '';
    $('span[name="S6"]')[0].innerHTML = '';

}
function convertToSign(signChar) {
    if (signChar == 'S') {
        return '<span style="color: black;font-size: 150%;">♠</span>'
    } else if (signChar == 'D') {
        //  return '♦';
        return '<span style="color: red;font-size: 150%;">♦</span>';
    } else if (signChar == 'C') {
        return '<span style="color: black;font-size: 150%;">♣</span>'
    } else if (signChar == 'H') {
        return '<span style="color: red;font-size: 150%;">♥</span>'
    } else {
        return '🚫';
    }
}
function passBid() {
    if (globalData.VSF.length == 0) {
        alert("Fist compulsory bid!!!");
        return;
    }
    if (globalData.VSF.length == 1) {
        let bidValue = Object.values(globalData.VSF[0])[0].substring(1);
        if (bidValue == '') {
            alert("Fist compulsory bid!!!");
            return;
        }
    }
    //let date = {};
    questionData.AnsNo = questionData.quNo;
    questionData.Answer = 'P';
    webSocket.send(JSON.stringify(questionData));
    $("#bidSection").hide();
    resetSpinner();

}
function sendBid() {
    var bidSign = $(".active").val();
    var bidValue = $("#bidValue").val();
    var moreBidDetails = $("#moreBidDetails").val();
    if (!validateBid(bidSign, bidValue)) {
        return;
    }
    //let data = {};
    questionData.AnsNo = questionData.quNo;
    questionData.Answer = bidSign + bidValue + moreBidDetails;
    webSocket.send(JSON.stringify(questionData));
    $("#bidSection").hide();
    resetSpinner();
}
function validateBid(bidSign, bidValue) {
    if (globalData.VSF.length > 0) {
        let vsfLength = globalData.VSF.length;
        let lastBidValue = '';
        while (lastBidValue == '' && vsfLength > 0) {
            let lastBid = globalData.VSF[vsfLength - 1];
            lastBidValue = Object.values(lastBid)[0].substring(1);
            vsfLength--;
        }

        if (bidValue <= lastBidValue) {
            alert("Invalid bid!!");
            return false;
        }
    }
    return true;
}
function getSeatNumber(seatNumber, pos) {
    return (seatNumber + pos === 6) ? 6 : ((seatNumber + pos) % 6)
};
function goToSeat(roomNo, seatNo) {
    seatNumber = parseInt(seatNo, 10);
    $("#activePlayer0")[0].innerHTML = "" + seatNo;
    $("#activePlayerName0").attr("name", "N" + seatNo);
    $("#playedCardS0").attr("name", "S" + seatNo);
    if (seatNumber % 2 == 0) {
        $("#playedCardS0").attr("style", "border:2px solid red");
    } else {
        $("#playedCardS0").attr("style", "border:2px solid black");

    }

    $("#viliPlayerS0").attr("name", "S" + seatNo);
    $("#spinnerS0").attr("name", "S" + seatNo);
    $("#foldButton").hide();


    let derivedSeatNumber = getSeatNumber(seatNumber, 1);
    $("#activePlayer1")[0].innerHTML = "" + derivedSeatNumber;
    $("#activePlayerName1").attr("name", "N" + derivedSeatNumber);

    $("#playedCardS1").attr("name", "S" + derivedSeatNumber);
    if (derivedSeatNumber % 2 == 0) {
        $("#playedCardS1").attr("style", "border:2px solid red");
    } else {
        $("#playedCardS1").attr("style", "border:2px solid black");

    }
    $("#viliPlayerS1").attr("name", "S" + derivedSeatNumber);
    $("#spinnerS1").attr("name", "S" + derivedSeatNumber);


    derivedSeatNumber = getSeatNumber(seatNumber, 2);
    $("#activePlayer2")[0].innerHTML = "" + derivedSeatNumber;
    $("#activePlayerName2").attr("name", "N" + derivedSeatNumber);

    $("#playedCardS2").attr("name", "S" + derivedSeatNumber);
    if (derivedSeatNumber % 2 == 0) {
        $("#playedCardS2").attr("style", "border:2px solid red");
    } else {
        $("#playedCardS2").attr("style", "border:2px solid black");

    }
    $("#viliPlayerS2").attr("name", "S" + derivedSeatNumber);
    $("#spinnerS2").attr("name", "S" + derivedSeatNumber);


    derivedSeatNumber = getSeatNumber(seatNumber, 3);
    $("#activePlayer3")[0].innerHTML = "" + derivedSeatNumber;
    $("#activePlayerName3").attr("name", "N" + derivedSeatNumber);

    $("#playedCardS3").attr("name", "S" + derivedSeatNumber);
    if (derivedSeatNumber % 2 == 0) {
        $("#playedCardS3").attr("style", "border:2px solid red");
    } else {
        $("#playedCardS3").attr("style", "border:2px solid black");

    }
    $("#viliPlayerS3").attr("name", "S" + derivedSeatNumber);
    $("#spinnerS3").attr("name", "S" + derivedSeatNumber);


    derivedSeatNumber = getSeatNumber(seatNumber, 4);
    $("#activePlayer4")[0].innerHTML = "" + derivedSeatNumber;
    $("#activePlayerName4").attr("name", "N" + derivedSeatNumber);

    $("#playedCardS4").attr("name", "S" + derivedSeatNumber);
    if (derivedSeatNumber % 2 == 0) {
        $("#playedCardS4").attr("style", "border:2px solid red");
    } else {
        $("#playedCardS4").attr("style", "border:2px solid black");

    }
    $("#viliPlayerS4").attr("name", "S" + derivedSeatNumber);
    $("#spinnerS4").attr("name", "S" + derivedSeatNumber);


    derivedSeatNumber = getSeatNumber(seatNumber, 5);
    $("#activePlayer5")[0].innerHTML = "" + derivedSeatNumber;
    $("#activePlayerName5").attr("name", "N" + derivedSeatNumber);

    $("#playedCardS5").attr("name", "S" + derivedSeatNumber);
    if (derivedSeatNumber % 2 == 0) {
        $("#playedCardS5").attr("style", "border:2px solid red");
    } else {
        $("#playedCardS5").attr("style", "border:2px solid black");

    }
    $("#viliPlayerS5").attr("name", "S" + derivedSeatNumber);
    $("#spinnerS5").attr("name", "S" + derivedSeatNumber);




    $("#seatSelection").hide();
    // http://127.0.0.1:5000/table?roomNo=1&seatNo=1&role=watcher

    if (window.location.toString().includes("role=watcher")) {
        webSocket = new WebSocket("ws://" + window.location.hostname + ":6789/watch?"
            + document.cookie + "&Room=" + roomNo + "&SeatNo=1"
        );

    }
    else {
        webSocket = new WebSocket("ws://" + window.location.hostname + ":6789/game?"
            + document.cookie + "&Room=" + roomNo + "&SeatNo=" + seatNo
        );
    }

    webSocket.onmessage = function (message) {
        console.log(message);
        if (message.data) {
            let data = JSON.parse(message.data);
            if (data.playsofar)
                globalData.playsofar = data.playsofar;
            if (data.VSF)
                globalData.VSF = data.VSF;
            if (data.hand)
                globalData.hand = data.hand;   // 3 ifs make sure that global data will not  saved and if any other events happens , it wont effect the game flow

            if (data.event == 'question') {
                resetPlayedCards();
                questionData = data;
                questionEvent(data);
                resetSpinner();
                //  console.log("questio  "+ data.SN)
                $("#spinnerS0").show();
                if (toggleAutoPassState) {
                    return passBid();
                }
            } else if (data.event == 'play') {
                globalData.playsofar = data.playsofar;
                globalData.VSF = data.VSF;
                globalData.hand = data.hand;
                playData = data;

                resetSpinner();
                $("#spinnerS0").show();
                if (folderButtonStatus) {
                    console.log("click on fold ");
                }
                else {
                    $("#playButton").attr("disabled", false);
                    $("#playSection").show();
                    if (globalData.hand.length ==1)
                        {
                                console.log("will do auto play");
                                playData.card = globalData.hand[0];
                                webSocket.send(JSON.stringify(playData));
                                $("#playButton").attr("disabled", true);
                                $("#playSection").hide();
                        }

                }

                if (data.base0) {
                    $("#team0")[0].innerHTML = data.base0;
                    $("#team1")[0].innerHTML = data.base1;
                    $('#gameCount')[0].innerHTML = data.Mc;

                }   // this when reconnect during action item
            } else if (data.event == 'MatchIsDone') {
                $("#team0")[0].innerHTML = data.base0;
                $("#team1")[0].innerHTML = data.base1;
                $('#gameCount')[0].innerHTML = data.Mc;
                $('div[id="foldSection"]').show();

                myNames = kunuguLogic(globalData.names, data.KunuguSeat);
                populateNames(myNames);

                $("#chat")[0].value += "\r\n" + "system" + ": " + data.dialoge;
                document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;

                turnAutoPassOff();
                $("#toggleAutoPassButton").show();
                $("#gameCount").attr("data-content", data.dialoge);
                $("#gameCount").popover(true, false, "", 5000, false, "left");
                setTimeout(function () { $("#gameCount").popover("hide"); }, 4000);
                $("#gameCount").popover("show");
                // To Mange Rest qame . Need to remove the question event
                if (data.dialoge.startsWith("Reset")) {
                    console.log("Will remove question");
                    $("#bidSection").hide();
                    $("#playButton").attr("disabled", true);
                    $("#foldButton").hide();
                }

            } else if (data.event == 'cardSend') {
                if (data.hand.length == 8) {

                    $("#playedCardS1").attr("src", "static/cards/RED_BACK.jpg");
                    $("#playedCardS2").attr("src", "static/cards/RED_BACK.jpg");
                    $("#playedCardS3").attr("src", "static/cards/RED_BACK.jpg");
                    $("#playedCardS4").attr("src", "static/cards/RED_BACK.jpg");
                    $("#playedCardS5").attr("src", "static/cards/RED_BACK.jpg");
                    $("#playedCardS6").attr("src", "static/cards/RED_BACK.jpg");
                    $("#playedCardS0").attr("src", "static/cards/RED_BACK.jpg");
                    $("#trumpSection")[0].innerHTML = "Bid : ";
                }

            } else if (data.event == 'HeGotPidi') {
                resetSpinner();
                $("#spinnerS" + data.spinner).show();
                if (data.who == data.my && role != 'watcher') {
                    $("#foldButton").show();
                    folderButtonStatus = true;
                }
            } else if (data.event == 'TrumpIsSet') {
                $("#viliPlayerS1").html("");
                $("#viliPlayerS2").html("");
                $("#viliPlayerS3").html("");
                $("#viliPlayerS4").html("");
                $("#viliPlayerS5").html("");
                $("#viliPlayerS6").html("");
                $("#viliPlayerS0").html("");

                $("#toggleAutoPassButton").hide();

            } else if (data.event == 'HeCalled') {
                if (data.Villi != "P") {
                    //console.log(data.dude);
                    //  console.log(data.dudeTeam);
                    $("#trumpSection")[0].innerHTML = "Bid " + convertToSign(data.Villi.substring(0, 1)) + data.Villi.substring(1) + " " + data.dude.substring(0, 12);

                    if (data.dudeTeam == 'Team1') {
                        $("#trumpSection")[0].style.color = "red";
                    }
                    else {
                        $("#trumpSection")[0].style.color = "black";  // coloring stuff added by st
                    }

                }
                showVili(data.VSF);
            } else if (data.event == 'spinner') {
                resetSpinner();
                $("#spinnerS" + data.spinner).show();

            } else if (data.event == 'fold') {
                console.log("Real fold");
                $("#foldButton").show();
                folderButtonStatus = true;
                foldData = data;

            } else if (data.event == 'Reconnect') {
                $("#team0")[0].innerHTML = data.base0;
                $("#team1")[0].innerHTML = data.base1;
                $('#gameCount')[0].innerHTML = data.Mc;
                resetSpinner();
                $("#spinnerS" + data.spinner).show();


                if (data.TrumpIsnotSet)
                    $("#toggleAutoPassButton").show();

                else
                    $("#toggleAutoPassButton").hide();

            } else if (data.event == 'chatSend') {
                let chatUser = data.usr;
                //data-content
                $("span:contains(" + chatUser + ")").attr("data-content", data.text);
                $("span:contains(" + chatUser + ")").popover(true, false, "sunu", 5000, false, "left");
                setTimeout(function () { $("span:contains(" + chatUser + ")").popover("hide"); }, 4000);
                $("span:contains(" + chatUser + ")").popover("show");
                $("#chat")[0].value += "\r\n" + data.usr + ": " + data.text;
                document.getElementById("chat").scrollTop = document.getElementById("chat").scrollHeight;
                if (data.role =="CPU")
                {

                  $("#trumpSection").attr("data-content","system:"+ data.text);
                  $("#trumpSection").popover(true, false, "", 5000, false, "left");
                  setTimeout(function () { $("#trumpSection").popover("hide"); }, 4000);
                  $("#trumpSection").popover("show");
                }
                else if (data.role =="w"){
                               $("#watechers").attr("data-content", chatUser+":"+data.text);
                               $("#watechers").popover(true, false, "", 5000, false, "left");
                               setTimeout(function () { $("#watechers").popover("hide"); }, 4000);
                               $("#watechers").popover("show");

                }


                //openForm();

            } // end of chat
            refreshHand(data);


        }  // end of event
        $("#playingTable").show();

    } // end of call back


    $("#playingTable").show();

} // end of go table html function


function questionEvent(data) {

    var higest = (data.loopStart);

    if (data.loopStart == 57)  // For thadiyan . Everyone will pass one villi is 56
    {
                   return passBid();

    }

    // if (data.VSF.length > 5 && data.loopStart < 40) {
    //     //console.log("will check for Pass&40");
    //     array_last_six = data.VSF.slice(-6);
    //     //console.log(array_last_six);
    //     for (var i = 5; i > 0; i--) {
    //         //console.log(array_last_six[i]);
    //         var key = (Object.keys(array_last_six[i]));
    //
    //         if (array_last_six[i][key] != "P") {
    //             // console.log(array_last_six[i][Object.keys(array_last_six[0][0]]);
    //             console.log(array_last_six[i]);
    //             SN = ((key[0][1]));
    //             // console.log(SN);
    //             // console.log(data.SN);
    //             // if ((data.SN - SN) % 2 == 0) {
    //             //     console.log("Same team");
    //             //     $("#gameCount").attr("data-content", "Second Round & Same team --> call 40");
    //             //     $("#gameCount").popover(true, false, "", 5000, false, "left");
    //             //     setTimeout(function () { $("#gameCount").popover("hide"); }, 4000);
    //             //     $("#gameCount").popover("show");
    //             //     //higest=40 // Can be cooment if not ok with
    //             // }
    //             // else
    //             //     console.log("differnt  team");
    //
    //             break;
    //         }
    //
    //     }
    // }// end of  checking condition for second round


    var contents;
    for (i = higest; i < 57; i++) {
        if (i == 28) {
            contents += "<option selected value=\"" + i + "\">" + i + "</option>";

        } else {
            contents += "<option value=\"" + i + "\">" + i + "</option>";
        }
    }
    $("#bidValue")[0].innerHTML = contents;
    $("#bidSection").show();
    $("#playSection").hide();
    $("#playButton").attr("disabled", true);

    if (data.base0) {
        $("#team0")[0].innerHTML = data.base0;
        $("#team1")[0].innerHTML = data.base1;
        $('#gameCount')[0].innerHTML = data.Mc;

    }  // Reconect during question event

}

function playEvent() {

    if (data.playsofar && data.playsofar.length == 0) {
        // $('div[id="foldSection"]').show();
    }
    $("#playButton").attr("disabled", false);
    $("#playSection").show();


}

function selectCard(card) {
    $(".card").removeClass("selectedCard");
    $(card).addClass("selectedCard");
    let name = ($(card).attr("name"));    // Added by Urmi

    console.log(globalData.hand);

    if (name.startsWith("H")) {
        selectSuit($("#heart"));
        nereOrThirichu("H");


    } else if (name.startsWith("C")) {
        selectSuit($("#club"));
        nereOrThirichu("C");
    } else if (name.startsWith("D")) {
        selectSuit($("#diamond"));
        nereOrThirichu("D");
    } else {
        selectSuit($("#spade"));
        nereOrThirichu("S");
    }

} // end of selectCard

function nereOrThirichu(name) {
    var startsWithCard = globalData.hand.filter((mycard) => mycard.startsWith(name));
    var found = false;
    //  console.log(startsWithCard);
    for (var i = 0; i < startsWithCard.length; i++) {
        if (startsWithCard[i][1] == "J") {
            console.log("Jack ");

            found = true;
            break;
        }
    }

    if (found)
        $("#moreBidDetails").val("⇧");
    else
        $("#moreBidDetails").val("↺");

}

function selectSuit(suit) {
    $('input[type=image]').removeClass('active');
    $('input[type=image]').addClass('inactive');
    suit.removeClass('inactive');
    suit.addClass('active');
}

function play() {
    $("#playedActiveCard").attr("src", $(".selectedCard").attr("src"));
    var selectedCard = $(".selectedCard").attr("name");
    var validPlay = validatePlay(selectedCard);
    if (!validPlay) {
        return;
    }
    playData.card = selectedCard;
    //alert(data.card);
    webSocket.send(JSON.stringify(playData));

    $(".selectedCard").remove();
    //$("#playSection").hide();

    $("#playButton").attr("disabled", true);
    $("#playSection").hide();
}
function validatePlay(card) {
    if (globalData.playsofar) {
        if (globalData.playsofar.length > 0) {
            var firstCard = Object.values(globalData.playsofar[0])[0];
            if (card.substring(0, 1) != firstCard.substring(0, 1)) {
                if (ifSignPresent(firstCard)) {
                    alert("Invalid play!!")
                    return false;
                }
            }
        }
    }
    return true;
}
function ifSignPresent(firstCard) {
    for (var i = 0; i < globalData.hand.length; i++) {
        if (globalData.hand[i].substring(0, 1) == firstCard.substring(0, 1)) {
            return true;
        }
    }
}
function resetPlayedCards() {
    for (i = 0; i < 6; i++) {
        $("#playedCardS" + i).attr("src", "static/cards/RED_BACK.jpg");    // for flask
    }
}

function showOtherCards(otherCards) {

    resetPlayedCards();

    for (i = otherCards.length - 1; i > -1; i--) {
        $('img[name="' + Object.keys(otherCards[i])[0] + '"]')
            .attr("src", "static/cards/" + otherCards[i][Object.keys(otherCards[i])[0]] + ".svg");   // for flask
    }
}
function fold() {
    //showOtherCards(data.playsofar);
    console.log("inside the fold");
    $("#playButton").attr("disabled", false);
    $("#playSection").show();

    $("#foldButton").hide();
    folderButtonStatus = false;
    if (foldData.fid) {
        foldData.FR = "P";
        webSocket.send(JSON.stringify(foldData));
        foldData={}; // To make Gloabl FoldData to empty

    }
}
jQuery(document).ready(function ($) {
    console.log(document.location.href);
    var queryString = document.location.href.split('?');
    var vars = queryString[1].split('&');
    var params = {};
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        params[pair[0]] = decodeURIComponent(pair[1]);
    }
    user = params["user"];
    if (!user) {
        try {
            user = document.cookie.split("=")[1];
        } catch (err) {

        }
    }
    roomNo = params["roomNo"];
    seatNo = params["seatNo"];                 //http://127.0.0.1:5000/table?user=joe&roomNo=1&seatNo=1
    role = params["role"];
    goToSeat(roomNo, seatNo);
//  Disabling reset base
      if ( (seatNo == 5) || (seatNo == 6) || (seatNo == 4) || (seatNo == 3) ) // Only seat 1 &2 power to reset the game
             $("#resetButton").attr("disabled", true);



    $('input[type=image]').click(function () {
        $('input[type=image]').removeClass('active');
        $('input[type=image]').addClass('inactive');
        $(this).removeClass('inactive');
        $(this).addClass('active');
    });


}); // end of Jquery Ready

function doBaseReset() {
    var resetRequest = {};
    resetRequest.resetID = "RestRequest";
    resetRequest.usr = user;
    resetRequest.r = roomNo;
    resetRequest.SN = seatNo;
    if (confirm("Do you want to Reset the base? One player form other team needs to do the same")) {
        webSocket.send(JSON.stringify(resetRequest));
    }

}


function sendChat() {
    var chatText = $("#chatText").val();
    $("#chatText").val("");

    var chatObject = {};
    chatObject.usr = user;
    chatObject.text = chatText;
    chatObject.chatID = "";
    chatObject.r = roomNo;
    console.log(role);
    if(role == "watcher")
     chatObject.role="w";
    console.log(chatObject) ;
    webSocket.send(JSON.stringify(chatObject));
    //notifyMe();
}

function goTolobby() {
    var resetRequest = {};
    resetRequest.gotoLobbyID = "GotoLooby";
    resetRequest.usr = user;
    resetRequest.r = roomNo;
    resetRequest.SN = seatNo;
    webSocket.send(JSON.stringify(resetRequest));

    const url = new URL(document.location.href);

    myURL = "http://" + url.hostname + ":" + url.port + "/lobby";

    document.location.href = myURL;


}


function notifyMe() {
    // Let's check if the browser supports notifications
    if (!("Notification" in window)) {
        alert("This browser does not support desktop notification");
    }

    // Let's check whether notification permissions have already been granted
    else if (Notification.permission === "granted") {
        // If it's okay let's create a notification
        var notification = new Notification("Hi there!");
    }

    // Otherwise, we need to ask the user for permission
    else if (Notification.permission !== "denied") {
        Notification.requestPermission().then(function (permission) {
            // If the user accepts, let's create a notification
            if (permission === "granted") {
                var notification = new Notification("Hi there!");
            }
        });
    }

    // At last, if the user has denied notifications, and you
    // want to be respectful there is no need to bother them any more.
}

function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function turnAutoPassOff() {
    toggleAutoPassState = false;
    $("#toggleAutoPassButton").removeClass("btn-danger");
    $("#toggleAutoPassButton")[0].innerHTML = "Pass Off";
    $("#toggleAutoPassButton").addClass("btn-primary");
}

function toggleAutoPass() {
    if (toggleAutoPassState) {
        toggleAutoPassState = false;
        $("#toggleAutoPassButton").removeClass("btn-danger");
        $("#toggleAutoPassButton")[0].innerHTML = "Pass Off";
        $("#toggleAutoPassButton").addClass("btn-primary");

    } else {
        toggleAutoPassState = true;
        $("#toggleAutoPassButton").addClass("btn-danger");
        $("#toggleAutoPassButton")[0].innerHTML = "Pass On";

        $("#toggleAutoPassButton").removeClass("btn-primary");
    }
}

function heartbeat() {
    // For better connection
    if (!webSocket) {
        return;
    }
    if (webSocket.readyState !== 1) return;
    var HeartBeat = {};
    HeartBeat.HBID = ""  // HBID
    webSocket.send(JSON.stringify(HeartBeat));
    setTimeout(heartbeat, 120000);  // 10 second , Which will increase to 1 or 2 min

}
