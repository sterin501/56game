jQuery(document).ready(function ($) {
    if (typeof $ == 'undefined') {
        var $ = jQuery;
    }
});
var user;
function goToTables() {
    user = $("#user").val();
    if(!user || user ==''){
        alert("Please enter username!!");
        return;
    }
    document.location.href = document.location.href.replace("login", "56") + "?user=" + user;
}

