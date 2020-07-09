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
var names;
console.log(uuid);
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
        if (data.dudeTeam == 'Team0') {
            team = "Black"
        }
        $("#trumpSection")[0].innerHTML = "Bid : " + team + " " + data.villi + convertToSign(data.trump);
    }

    if (data.playsofar && data.playsofar.length != 0) {
        showOtherCards(data.playsofar);
    }
    if (data.VSF && (!globalData.playsofar || globalData.playsofar.length == 0)) {
        showVili(data.VSF);
    }

    if(data.names){
        populateNames(data.names);
    }


}

function populateNames(names) {
    $('span[name="N1"]')[0].innerHTML = names["SN1"];
    $('span[name="N2"]')[0].innerHTML = names["SN2"];
    $('span[name="N3"]')[0].innerHTML = names["SN3"];
    $('span[name="N4"]')[0].innerHTML = names["SN4"];
    $('span[name="N5"]')[0].innerHTML = names["SN5"];
    $('span[name="N6"]')[0].innerHTML = names["SN6"];


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
        return '♠';
    } else if (signChar == 'D') {
        return '♦';
    } else if (signChar == 'C') {
        return '♣';
    } else if (signChar == 'H') {
        return '♥';
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
    if (!validateBid(bidSign, bidValue)) {
        return;
    }
    //let data = {};
    questionData.AnsNo = questionData.quNo;
    questionData.Answer = bidSign + bidValue;
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
    //$('#toast').toast('show');
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
    //console.log(folderButtonStatus);


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
    //document.cookie = seatNo;
    console.log(document.cookie);
    webSocket = new WebSocket("ws://" + window.location.hostname + ":6789/game?"
        + document.cookie + "&Room=" + roomNo + "&SeatNo=" + seatNo
    );

    console.log(webSocket);

    webSocket.onmessage = function (message) {
        console.log(message);
        if (message.data) {
            //$('div[id="foldSection"]').hide();
            let data = JSON.parse(message.data);
            globalData.playsofar = data.playsofar;
            globalData.VSF = data.VSF;
            globalData.hand = data.hand;
            if (data.event == 'question') {
                resetPlayedCards();
                questionData = data;
                questionEvent(data);
                resetSpinner();
                //  console.log("questio  "+ data.SN)
                $("#spinnerS0").show();


            }
            if (data.VSF) {
                globalData.VSF = data.VSF;
            }
            refreshHand(data);
            //$("#toastMessage")[0].innerHTML = data.message;
            //$("#myToast").toast('show');

            if (data.event == 'play') {
                globalData.names = data.names;
                globalData.playsofar = data.playsofar;
                globalData.VSF = data.VSF;
                globalData.hand = data.hand;
                playData = data;
               
                resetSpinner();
                $("#spinnerS0").show();
                console.log(folderButtonStatus);
                if (folderButtonStatus) { console.log("click on fold "); }
                else { $("#playButton").attr("disabled", false); }


            }
            if (data.event == 'MatchIsDone') {
                $("#team0")[0].innerHTML = data.base0;
                $("#team1")[0].innerHTML = data.base1;
                $('#gameCount')[0].innerHTML = data.Mc;
                $('div[id="foldSection"]').show();



            }

            if (data.event == 'cardSend') {

                // console.log("card send ");
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

            }
            if (data.event == 'HeGotPidi') {

                //  $('div[name="' + data.message + '"]').show();
                resetSpinner();
                $("#spinnerS" + data.spinner).show();
                if (data.who == data.my) {
                    console.log("fold")
                    $("#foldButton").show();
                    folderButtonStatus = true;

                }
            }
            if (data.event == 'TrumpIsSet') {
                $("#viliPlayerS1").html("");
                $("#viliPlayerS2").html("");
                $("#viliPlayerS3").html("");
                $("#viliPlayerS4").html("");
                $("#viliPlayerS5").html("");
                $("#viliPlayerS6").html("");
                $("#viliPlayerS0").html("");

            }
            if (data.event == 'HeCalled') {
                if (data.Villi != "P") {
                    $("#trumpSection")[0].innerHTML = "Bid : " + convertToSign(data.Villi.substring(0, 1)) + data.Villi.substring(1);

                }
            }

            if (data.event == 'spinner') {
                resetSpinner();
                // console.log("Seat No  "+ data.spinner);
                //   $("#spinnerS"+((data.spinner+6-data.myseat)%6).toString()).show();
                $("#spinnerS" + data.spinner).show();

            } // spinner

            if (data.event == 'fold') {
                console.log("Real fold");
                $("#foldButton").show();
                folderButtonStatus = true;
                foldData = data;

            } // spinner


        }  // end of event
        $("#playingTable").show();

    } // end of call back


    $("#playingTable").show();

} // end of go table html function


function questionEvent(data) {

    var higest = (data.loopStart);
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
    //$("#playSection").hide();
    $("#playButton").attr("disabled", true);

}

function playEvent() {

    if (data.playsofar && data.playsofar.length == 0) {
        // $('div[id="foldSection"]').show();
    }
    $("#playButton").attr("disabled", false);

}

function selectCard(card) {
    $(".card").removeClass("selectedCard");
    $(card).addClass("selectedCard");
    let name = ($(card).attr("name"));
    if (name.startsWith("H")) {
        selectSuit($("#heart"));
    } else if (name.startsWith("C")) {
        selectSuit($("#club"));
    } else if (name.startsWith("D")) {
        selectSuit($("#diamond"));
    } else {
        selectSuit($("#spade"));
    }
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
    $("#foldButton").hide();
    folderButtonStatus = false;
    if (foldData.fid) {
        foldData.FR = "P";
        webSocket.send(JSON.stringify(foldData));

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
    roomNo = params["roomNo"];
    seatNo = params["seatNo"];                 //http://127.0.0.1:5000/table?user=joe&roomNo=1&seatNo=1
    goToSeat(roomNo, seatNo);
    $('input[type=image]').click(function () {
        $('input[type=image]').removeClass('active');
        $('input[type=image]').addClass('inactive');
        $(this).removeClass('inactive');
        $(this).addClass('active');
    });
});
