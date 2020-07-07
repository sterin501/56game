    jQuery(document).ready(function ($) {
        if (typeof $ == 'undefined') {
            var $ = jQuery;
        }
    });
    var user;
    function goToSeatSelection() {
        user = $("#user").val();
        $("#loginSection").hide();
        $('#tableSection').load('table.html');

    }

