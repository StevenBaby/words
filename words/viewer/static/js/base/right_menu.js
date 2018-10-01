$(".right-menu-item.logout").click(function(){
    var logout = $(this);
    dialog({
        title_color : "red",
        description : gettext("Really want to logout ?"),
        description_color : "red",
        onApprove : function() {
            var logout_url = logout.find("input").get(0).value;
            //console.log(logout_url);
            $(window.location).attr('href', logout_url);
        }
    });
});