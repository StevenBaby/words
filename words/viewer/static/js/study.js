reviewed = false;
practice = false;
title = "";
index = 0;
input_disabled = false;

function play(phonetic) {
    title = $(phonetic).attr("value");
    type = $(phonetic).attr("type");
    icon = $(phonetic).find("i.icon");

    url = "/phonetic/{0}/{1}".format(type, title);
    var audio = new Audio(url);
    audio.onplay = function () {
        // console.log(icon);
        icon.removeClass("down up");
        icon.addClass("up");
    };
    audio.onended = function () {
        icon.removeClass("down up");
        icon.addClass("down");
        // console.log(icon);
    };
    audio.play();
}

function random_play() {
    if (phonetics.length < 1)
        return;
    i = Math.floor(Math.random() * phonetics.length);
    phonetic = phonetics[i];
    play(phonetic);
}

function next_play() {
    phonetics = $(".phonetic");
    if (phonetics.length < 1)
        return;
    index = (index + 1) % phonetics.length;
    phonetic = phonetics[index];
    play(phonetic);
}

$("body").on("click", ".study.phonetic", function () {
    play(this);
});

function reset_input() {
    $("input.study").val("");
    $("input.study").focus();
}

$(document).ready(function () {
    phonetics = $(".phonetic");
    index = Math.floor(Math.random() * phonetics.length);
    action = $("#action").val();
    if (action == "next") {
        reset_input();
    }

    method = $(".study.method");
    if (method.length < 1) {
        return;
    }
    if (method.attr("method") == 'dictation') {
        next_play();
    }

});



function get_para(paras) {
    if (!paras) {
        return "";
    }
    para = "| ";
    for (var i = 0; i < paras.length; i++) {
        para += "{0}. {1} | ".format(paras[i][0], paras[i][1]);
    }
    return para;
}


function get_diff(line) {
    var ignores = /[ \.,\?\-']/g;
    let i = 0;
    let j = 0;
    for (i = 0; i < line.length;) {
        if (j >= title.length)
            break;
        let l = line[i];
        let t = title[j];

        if (l.match(ignores)) {
            i++;
            continue;
        }
        if (t.match(ignores)) {
            j++;
            continue;
        }
        if (l.toLowerCase() != t.toLowerCase()) {
            break;
        }
        i++;
        j++;
    }
    var before = line.slice(0, i);
    var after = line.slice(i);
    var result = before.strip() + ' | ' + after.strip();
    console.log(result);
    return result;
}

function get_check_line(item) {
    if (item.error == undefined || !item.error)
        return "{0} {1}".format(item.title, get_para(item.paras))
    return get_diff(item.title);
}

function append_check_item(item, style) {
    button = $(".study.check.example").clone();
    button.appendTo($('div.study.check.list'));
    button.removeClass("example");
    button.addClass(style);
    button.find("a").html(get_check_line(item));
    button.find("a").addClass(style);
    button.find("a").attr("href", "/found/{0}/".format(item.title))
    button.show();
}

function show_check_list(data) {
    if (data.error) {
        practice = true;
        title = data.title;
        $(".word.mark i").attr("class", "write icon");
        $(".word.mark span").html(gettext("PR"));
    }
    reviewed = true;
    if (!data.equal) {
        data.error = false;
        append_check_item(data, "");
    }
    for (var index = 0; index < data.list.length; index++) {
        var item = data.list[index]
        if (item.equal) {
            append_check_item(item, "green");
        } else if (item.right) {
            append_check_item(item, "teal");
        } else if (item.exists) {
            append_check_item(item, "yellow");
        } else if (item.error) {
            append_check_item(item, "red");
        }
    }
    $('div.study.check.list').transition('slide down in');
    // $('.study.paraphrase').transition('slide down in');
}

var checking = false;

function check(input) {
    var t = title.toLowerCase();
    var i = input.toLowerCase();
    if (t == i)
        return true;
    var ignores = /[ \.,\?\-']/g;
    if (t.replace(ignores, '') == i.replace(ignores, ''))
        return true;
    return false;
}

$("input.study").keydown(function (event) {
    if (checking)
        return;
    if (event.keyCode == 120) { // F9 to play audio
        next_play();
        return;
    }
    if (event.keyCode != 13)
        return;
    form = $('.ui.study.form');
    input_line = $("input.study").val().strip();
    method = $(".study.method");

    if (practice && !check(input_line)) {
        if (input_line != "") {
            item = {
                title: input_line,
                error: true,
            }
            append_check_item(item, "pink");
        }
        reset_input();
        return;
    } else {
        practice = false;
    }
    if (reviewed || input_line.toUpperCase() == "N") {
        location.reload();
        return;
    }
    if (input_line.toUpperCase() == "T" || input_line.toUpperCase() == 'TT') {
        // tt avoid input double t is nonsence
        reset_input();
        $('.study.paraphrase.table').transition('slide down');
        return
    }
    if (input_line.toUpperCase() == "I") {
        reset_input();
        $('.study.review.info.table').transition('slide down');
        return
    }
    if (input_line.length < 2) {
        reset_input();
        next_play();
        return;
    }

    form.find("input[name='input_line']").val(input_line);
    url = form.find(".action").get(0).value

    $("input.study").addClass('disabled');
    checking = true;
    $.ajax({
        url: url,
        type: "POST",
        async: true,
        data: form.serialize(),
        beforeSend: function (XMLHttpRequest) {},
        success: function (data) {
            $("input.study").val("");
            if (!data.success) {
                // toastr.warning(data.description);
                // setTimeout(function() {
                //     location.reload();
                // }, 850);
                location.reload();
            } else {
                show_check_list(data);
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {},
        complete: function (XMLHttpRequest, textStatus) {
            $("input.study").removeClass('disabled');
            checking = false;
        }
    });
});

$("body").on("click", ".button.paraphrase.detail", function () {
    $('.study.paraphrase.table').transition('slide down');
});

$("body").on("click", ".button.review.info", function () {
    $('.study.review.info.table').transition('slide down');
});

$("body").on("click", ".button.word.mark", function () {

});


var current_time = null;

function refresh_time() {
    time_span = $(".current.time");
    if (time_span.length < 1) {
        return;
    }
    if (!current_time) {
        current_time = new Date(time_span.html());
    }
    var interval = 1000;
    current_time.setTime(current_time.getTime() + interval);
    show_time = new Date(current_time);
    show_time.setMinutes(current_time.getMinutes() - current_time.getTimezoneOffset());
    show_time = show_time.toISOString().slice(0, 10) + " " + show_time.toISOString().slice(11, 19);
    time_span.html(show_time);
    // setTimeout(refresh_time, interval);
    show_time = null;
}

function PrefixInteger(num, length) {
    return ("0000000000000000" + num).substr(-length);
}

var countdown = null;

function refresh_countdown() {
    time_span = $(".study.countdown");
    if (time_span.length < 1) {
        return;
    }

    var seconds_label = $(".study.countdown.seconds");
    var seconds = parseInt(seconds_label.html())
    seconds -= 1;
    if (seconds >= 0) {
        seconds_label.html(PrefixInteger(seconds, 2));
        // setTimeout(refresh_countdown, 1000);
        return
    }
    seconds = 59;

    var minutes_label = $(".study.countdown.minutes");
    var minutes = parseInt(minutes_label.html())

    minutes -= 1;
    if (minutes >= 0) {
        seconds_label.html(PrefixInteger(seconds, 2));
        minutes_label.html(PrefixInteger(minutes, 2));
        // setTimeout(refresh_countdown, 1000);
        return
    }
    minutes = 59;

    var hours_label = $(".study.countdown.hours");
    var hours = parseInt(hours_label.html())
    hours -= 1
    if (hours >= 0) {
        seconds_label.html(PrefixInteger(seconds, 2));
        minutes_label.html(PrefixInteger(minutes, 2));
        hours_label.html(PrefixInteger(hours, 2));
        // setTimeout(refresh_countdown, 1000);
        return;
    }
    hours = 23;

    var days_label = $(".study.countdown.days");
    if (days_label.length <= 0) {
        setTimeout(function () {
            location.href = $(".study.start.url").attr("href");
        }, 1000);
        return;
    }

    seconds_label.html(PrefixInteger(seconds, 2));
    minutes_label.html(PrefixInteger(minutes, 2));
    hours_label.html(PrefixInteger(hours, 2));

    days = parseInt(days_label.find(".value").html());
    days -= 1;
    if (days > 0) {
        days_label.find(".value").html(days);
        // setTimeout(refresh_countdown, 1000);
        return;
    }
    days_label.remove();
    // setTimeout(refresh_countdown, 1000);
}

$(document).ready(function () {
    // refresh_time();
    // refresh_countdown();
    if ($(".current.time").length > 0) {
        setInterval(refresh_time, 1000);
    }
    if ($(".study.countdown").length > 0) {
        setInterval(refresh_countdown, 1000);
    }
})