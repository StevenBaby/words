// settings javascript

function set_phonetic_status(){
    var progress = $(".settings.phonetic.download.progress");
    var button = $(".settings.phonetic.download.button");
    $.ajax({
        url: '/settings/phonetic/status',
        type: "POST",
        async: true,
        success: function(data){
            progress.progress({
                percent: data.percent,
                text :{
                    active  : "( {0} / {1} )".format(data.value, data.total),
                }
            })
            if (data.downloading){
                setTimeout(set_phonetic_status, 1000);
            }else{
                button.removeClass("blue red");
                button.addClass("blue");
                button.find("i").removeClass("stop download");
                button.find("i").addClass("download");
                button.find("span").html(gettext("Download"));
            }
        },
    });
}

function set_updating_status(){
    var progress = $(".settings.updater.updating.progress");
    if (progress.length < 1){
        return;
    }
    $.ajax({
        url: '/settings/update/status',
        type: "POST",
        async: true,
        success: function(data){
            if (!data.updating){
                location.reload();
                return;
            }
            text = gettext("Finished");
            if (data.status == 'downloading'){
                text = gettext("Downloading");
            }
            else if (data.status == 'extracting'){
                text = gettext("Extracting");
            }
            else if (data.status == 'moving'){
                text = gettext("Moving");
            }
            progress.progress({
                percent: data.percent,
                text :{
                    active  : text,
                }
            })
        },
        complete: function(XMLHttpRequest, textStatus){
            setTimeout(set_updating_status, 1000);
        }
    });
}

$(document).ready(function(){
    set_phonetic_status();
    set_updating_status();
})


$(".settings.download.progress").progress();
$(".settings.updating.progress").progress();


$(".settings.backup.action").click(function(){
    button = $(this);
    form = $(".settings.backup.form");
    $.ajax({
        url: form.attr("action"),
        type: "GET",
        async: true,
        data: form.serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled"); },
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() { location.reload(); }, 500);
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
})

$(".settings.backup.restore").click(function(){
    button = $(this);
    form = $(".settings.restore.form");
    console.log(form.attr("action"));
    $.ajax({
        url: form.attr("action"),
        type: "GET",
        async: true,
        data: form.serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled"); },
        success: function(data){
            if (!data.success){
                toastr.warning(data.description);
                return;
            }
            toastr.success(data.description);
            setTimeout(function() { location.reload(); }, 500);
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
})

$(".settings.profile.save").click(function(){
    button = $(this);
    form = $(".settings.profile.form");
    console.log(form.attr("action"));
    console.log(form.serialize());
    $.ajax({
        url: form.attr("action"),
        type: "POST",
        async: true,
        data: form.serialize(),
        beforeSend : function(XMLHttpRequest){ button.addClass("disabled"); },
        success: function(data){
            // if (!data.success){
            //     toastr.warning(data.description);
            //     return;
            // }
            toastr.success(gettext("Save success"));
            setTimeout(function() { location.reload(); }, 500);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){
            toastr.warning(gettext("Save failure, please try again later"));
        },
        complete: function(XMLHttpRequest, textStatus){
            button.removeClass("disabled");
        }
    });
})