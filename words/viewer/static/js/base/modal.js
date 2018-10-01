var dialog = function(data) {
    var modal = $(".ui.modal");
    //console.log(data);
    if (!data){
        data = {};
    }
    data["blurring"] = true;
    if (data.title){
        modal.find(".title.header").text(data.title);
    }else{
        modal.find(".title.header").text(gettext('Notice'));
    }

    if (data.title_color){
        // console.log(data.title_color);
        modal.find(".title.header").attr("class", "ui header " + data.title_color);
    }else{
        modal.find(".title.header").attr("class", "ui header teal");
    }

    if (data.description){
        modal.find(".content .header").text(data.description);
    }else{
        modal.find(".content .header").text(gettext("System notice !!!" ));
    }

    if (data.description_color){
        modal.find(".content .header").attr("class", "ui header " + data.description_color);
    }else{
        modal.find(".content .header").attr("class", "ui header teal");
    }
    modal.modal(data).modal("show");
}