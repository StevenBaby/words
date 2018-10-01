// edit javascript

$("body").on("click", ".add.edit", function(){
    var button = $(this);
    var action = button.attr("action");
    if (!action){ return; }
    $.ajax({
        url: action,
        type: "POST",
        async: true,
        data : $(".add.form").serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled"); },
        success: function(data){
            var result = data;
            if (!data.success){
                toastr.warning(data.description);
                button.transition('slide up out');
                return;
            }
            toastr.success(data.description);
            var edit_label = button.siblings(".ui.pink.label.edit").first();
            if (edit_label.length < 1 && data.edit_url != undefined){
                edit_label = button.clone();
                edit_label.attr("href", data.edit_url)
                edit_label.html(gettext("Edit"))
                edit_label.attr("class", "ui pink label edit");
                edit_label.attr("target", "_blank");
                button.siblings(".add.form.wordcard").after(edit_label);
                edit_label.transition('slide down in');
            }
            if (data.action == 'word'){
                button.transition('slide up out');
            }
            if (data.action == 'review'){
                button.siblings(".add.edit.word").transition('slide up out');
                button.attr("class", 'ui teal tag label');
                button.attr("action", null);
                button.html(gettext("Already in review"));
            }
            // modify resources list tag information 
            var wordcard = button.closest('tr.resource.wordcard');
            // console.log(wordcard);
            if (wordcard.length < 1){
                return;
            }
            var tr = wordcard.prev("tr.resource.item");
            var tag = tr.find(".tiny.label.tag");
            tag.transition("slide up out");
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
});


function deal_edit_remove(action, form, button)
{
    $.ajax({
        url: action,
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled") },
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            if (data.action == "para"){
                button.closest("tr").transition('slide up out');
                setTimeout(function() {
                    button.closest("tr").remove();
                }, 200);
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){
            if(action.indexOf("word") != -1){
                $(".edit.remove").transition('slide up out');
                setTimeout(function() {
                     self.location = '/found/';
                }, 800);
                return;
            }
            else if (action.indexOf("review") != -1) {
                $(".edit.remove.reset").transition('slide up out');
                button.transition('slide up out');
            }
            else if (action.indexOf("reset") != -1)
            {
                button.removeClass("disabled");
            }
        }
    });
}


$("body").on("click", ".edit.remove", function(){
    button = $(this);
    action = button.attr("action");
    is_alert = button.attr("alert");
    if (!action){
        return;
    }
    form = $(".remove.form");

    var description = "";
    if (action.indexOf("reset") != -1)
    {
        description = gettext("Really want to reset this review?")
    }
    else if (action.indexOf("word") != -1)
    {
        description = gettext("Really want to delete this word?")
    }
    else if (action.indexOf("review") != -1)
    {
        description = gettext("Really want to remove this review?")
    }
    else if (action.indexOf("para") != -1){
        description = gettext("Really want to remove this paraphrase?")
    }
    // console.log(is_alert);
    if (is_alert == "True")
    {
        dialog({
            title_color : "red",
            description : description,
            description_color : "red",
            onApprove : function() {
                deal_edit_remove(action, form, button);
            }
        });
    }
    else{
        deal_edit_remove(action, form, button);
    }
});


$("body").on("click", ".edit.refresh", function(){
    button = $(this);
    form = $(".refresh.form");
    $.ajax({
        url: form.attr("action"),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled") },
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() {
                location.reload()
            }, 300);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
});


function show_paraphrase_form(element, show){
    button = element.closest("tr").find(".edit.paraphrase.save");
    button.addClass("disabled");
    icon = button.find("i");
    span = button.find("span");
    label = button.closest("tr").find(".edit.paraphrase.label");
    form = button.closest("tr").find(".edit.paraphrase.form");

    if (show == null){
        if (icon.hasClass("edit")) {
            show = true;
        }else{
            show = false;
        }
    }
    if(show){ // show edit form
        icon.removeClass("edit save");
        icon.addClass("save");
        span.html(gettext("Save"));

       label.transition({duration : 0});
       form.transition({
            animation  : 'vertical flip in',
            duration   : '300ms',
            onComplete : function() {
                button.removeClass("disabled");
            }
        });
    }
    else{
        icon.removeClass("save edit");
        icon.addClass("edit");
        span.html(gettext("Edit"));
        form.transition({duration : 0});
        label.transition({
            animation  : 'vertical flip in',
            duration   : '300ms',
            onComplete : function() {
                button.removeClass("disabled");
            }
        }); 
    }
}


function save_paraphrase_request(form){
    // console.log(form);
    $.ajax({
        url: form.attr('action'),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){},
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){}
    });
}


function save_paraphrase(element){
    form = element.closest("tr").find(".edit.paraphrase.form");
    type_label = element.closest("tr").find(".edit.paraphrase.label .type");
    para_label = element.closest("tr").find(".edit.paraphrase.label .paraphrase");
    before_type = type_label.html().strip();
    before_para = para_label.html().strip();
    
    // console.log("before_type " + before_type);
    // console.log("before_para " + before_para);

    after_type = form.find("input[name='para_type']").val().strip();
    after_para = form.find("input[name='para_content']").val().strip();
    
    // console.log("after_type " + after_type);
    // console.log("after_para " + after_para);

    if(after_type){
        type_label.html(after_type);
    }
    else{
        toastr.warning(gettext("Paraphrase type must not empty."))
        return false;
    }
    if (after_para){
        para_label.html(after_para);
    }
    else{
        toastr.warning(gettext("Paraphrase must not empty."))
        return false;
    }   
    if (before_type == after_type && before_para == after_para){
        return true;
    }
    save_paraphrase_request(form);
    return true;
}

$("body").on("dblclick", ".edit.paraphrase.label", function(){
    show_paraphrase_form($(this), true);
})

$("body").on("keydown", ".edit.paraphrase.form input", function(event){
    if(event.keyCode !=13)
        return;
    input = $(this);
    if(save_paraphrase(input)){
        show_paraphrase_form(input, false);
    }
});

$("body").on("click", ".edit.paraphrase.save", function(){
    button = $(this);
    icon = button.find("i");
    if (icon.hasClass("edit")) {
        show_paraphrase_form(button, true);
        return;
    }
    if(save_paraphrase(button)){
        show_paraphrase_form(button, false);
    }
});



function add_paraphrase(element){
    form = element.closest("tr").find(".add.paraphrase.form");
    para_type = form.find("input[name='para_type']").val().strip();
    para_content = form.find("input[name='para_content']").val().strip();

    if (!para_type){
        toastr.warning(gettext("Paraphrase type must be not empty."));
        return;
    }
    
    if (!para_content){
        toastr.warning(gettext("Paraphrase content must be not empty."));
        return;
    }
    $.ajax({
        url: form.attr('action'),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){},
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() {location.reload();}, 300);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){}
    });
}



$(".add.paraphrase.form input").keydown(function(event){
    if(event.keyCode !=13)
        return;
    input = $(this);
    add_paraphrase(input);
});


$("body").on("click", ".edit.paraphrase.add", function(){
    add_paraphrase($(this))
});


$("body").on("click", ".edit.equal.word.save", function(){
    form = $(".edit.equal.word.form");
    $.ajax({
        url: form.attr('action'),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){},
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() {location.reload();}, 300);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){}
    });
});


$('.ui.dropdown.equal.word').dropdown({
    apiSettings: {
        url: '/search/{query}',
    },
    fields: {
        name    : 'title' ,
        value   : 'id'
    },
    saveRemoteData: false,
});

$("body").on("click", ".edit.similar.word.save", function(){
    form = $(".edit.similar.word.form");
    // console.log(form.find("select").val());
    $.ajax({
        url: form.attr('action'),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){},
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() {location.reload();}, 300);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){}
    });
});


$('.ui.dropdown.similar.word').dropdown({
    apiSettings: {
        url: '/search/{query}',
    },
    fields: {
        name    : 'title' ,
        value   : 'id'
    },
    saveRemoteData: false,
});


$("body").on("click", ".edit.related.word.save", function(){
    form = $(".edit.related.word.form");
    // console.log(form.find("select").val());
    $.ajax({
        url: form.attr('action'),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){},
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() {location.reload();}, 300);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){}
    });
});


$('.ui.dropdown.related.word').dropdown({
    apiSettings: {
        url: '/search/{query}',
    },
    fields: {
        name    : 'title' ,
        value   : 'id'
    },
    saveRemoteData: false,
});

function show_title_form(element, show){
    button = element.closest("tr").find(".edit.title.save");
    button.addClass("disabled");
    title_label = element.closest("tr").find(".edit.title.bar .title");
    input = element.closest("tr").find("input.edit.title");
    icon = button.find("i");
    span = button.find("span");
    label = button.closest("tr").find(".edit.title.bar");
    form = button.closest("tr").find(".edit.title.form");

    if (show == null){
        if (icon.hasClass("edit")) {
            show = true;
        }else{
            show = false;
        }
    }
    if(show){ // show edit form
        icon.removeClass("edit save");
        icon.addClass("save");
        span.html(gettext("Save"));
        input.val(title_label.html().strip());
        label.transition({duration : 0});
        form.transition({
            animation  : 'vertical flip in',
            duration   : '300ms',
            onComplete : function() {
                button.removeClass("disabled");
            }
        });
    }
    else{
        icon.removeClass("save edit");
        icon.addClass("edit");
        span.html(gettext("Edit"));
        form.transition({duration : 0});
        label.transition({
            animation  : 'vertical flip in',
            duration   : '300ms',
            onComplete : function() {
                button.removeClass("disabled");
            }
        }); 
    }
}

function save_title_request(form){
    title_label = form.closest("tr").find(".edit.title.bar .title");
    before_title = form.find(".edit.title.before").val();
    $.ajax({
        url: form.attr('action'),
        type: "POST",
        async: true,
        data : form.serialize(),
        beforeSend : function(XMLHttpRequest){},
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                title_label.html(before_title);
                return;
            }
            toastr.success(data.description);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            console.log(errorThrown);
        },
        complete: function(XMLHttpRequest, textStatus){}
    });
}

function save_title(element) {
    form = element.closest("tr").find(".edit.title.form");
    title_label = element.closest("tr").find(".edit.title.bar .title");
    before_title = title_label.html().strip();
    // console.log("before_title " + before_title);
    after_title = form.find("input[name='title']").val().strip();
    // console.log("after_title " + after_title);
    if(after_title){
        title_label.html(after_title);
    }
    else{
        toastr.warning(gettext("Word title must not empty."))
        return false;
    }
    if (before_title == after_title){
        return true;
    }
    save_title_request(form);
    return true;
}

$("body").on("click", ".edit.title.save", function(){
    button = $(this);
    icon = button.find("i");
    if (icon.hasClass("edit")) {
        show_title_form(button, true);
        return;
    }
    if(save_title(button)){
        show_title_form(button, false);
    }
});

$("body").on("keydown", "input.edit.title", function(event){
    if(event.keyCode !=13)
        return;
    input = $(this);
    if (save_title(input)) {
        show_title_form(input, false);
    };
});