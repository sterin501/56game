jQuery(document).ready(function ($) {
    if (typeof $ == 'undefined') {
        var $ = jQuery;
    }
});
var user;
function goToTables() {
    user = $("#user").val();
    $("#loginSection").hide();
    $('#tableSection').load('static/js/table.html');
    //$("#tableSection").show();
    // var bidValue = $("#bidValue").val();

    // if (!validateBid(bidSign, bidValue)) {
    //     return;
    // }
    // //let data = {};
    // questionData.AnsNo = questionData.quNo;
    // questionData.Answer = bidSign + bidValue;
    // webSocket.send(JSON.stringify(questionData));
    // $("#bidSection").hide();
    // resetSpinner();
}
