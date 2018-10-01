$("input.found").keydown(function(event){
    if(event.keyCode !=13)
        return;
    input_line = $("input.found").val().strip();
    if(input_line.length < 2){
        toastr.warning(gettext("Please input at least two letters."))
        return;
    }
     window.location = "/found/{0}".format(input_line);
});


$("body").on("click", ".item.resource.list", function(){
    item = $(this);
    action = item.attr("action");
    query = item.attr("value") + "/"
    while(true){
        item = item.parent().closest(".item.resource");
        if (!item.attr("value"))
            break;
        query = item.attr("value") + "/" + query;
        // console.log(query);
    }
    url = action + query;
    window.open(url); 
    // window.location = url;
});


$(document).ready(function(){
    $("input.found").val("");
    $("input.found").focus();
});


$(document).ready(function(){
    var checkboxs = $('.dictionary .checkbox');
    // console.log(checkboxs);
    for(var i = 0 ; i < checkboxs.length; ++i)
    {
        var checkbox = $(checkboxs[i]);
        var check = "uncheck";
        if(checkbox.hasClass('checked')){
            check = 'check';
        }
        checkbox.checkbox(check).checkbox({
            onChecked: function() {
                // console.log($(this).attr("action"));
                window.location = $(this).attr("action");
            },
            onUnchecked: function() {
                // console.log($(this).attr("action"));
                window.location = $(this).attr("action");
            },
        });
    }
});


$("body").on("click", ".resource.add.review", function(){
    var button = $(this);
    var action = button.attr("action");
    if (!action){ return; }

    var tr = button.closest("tr");
    var tag = tr.find(".tiny.label.tag")
    $.ajax({
        url: action,
        type: "POST",
        async: true,
        data : $(".add.form.resource").serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled"); },
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                button.transition('slide up out');
                return;
            }
            toastr.success(data.description);
            if (data.action == 'review'){
                button.attr("class", "ui green tiny label tag");
                button.attr("action", null);
                button.html(gettext("Already in review"));
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
});

$("body").on("click", ".resource.information", function(){
    var button = $(this);
    var action = button.attr("action");
    var tr = button.closest("tr");
    var card = tr.next(".wordcard");
    if(card.length > 0){
        card.transition('slide down');
        return;
    }
    // console.log($(".resource.wordcard"));

    card = $(".resource.wordcard.example").clone();
    card.removeClass("example");

    $.ajax({
        url: action,
        type: "GET",
        async: true,
        data : null,
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled"); },
        success: function(data){
            card.find(".content").html(data);
            tr.after(card);
            card.transition("slide down in");
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
});