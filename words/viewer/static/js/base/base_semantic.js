//set language
$(".select-language form > a").click(function (){
    $(this).closest("form").submit();
});

$('.message .close').click(function() {
    $(this).closest('.message').transition('fade');
    $(this).closest('.message').remove();
});

$('.selection.ui.dropdown').dropdown();

$('.pop').popup();

$('.menu .ui.dropdown').dropdown({
     action: 'hide',
      // transition: 'drop',
 });

$('.ui.embed').embed();


// $(".image.avatar").click(function(){
//     var index = Math.floor(Math.random()*10);
//     switch(index){
//         case 1:
//             $(this).transition("tada");
//             break;
//         case 1:
//             $(this).transition("flash");
//             break;
//         case 2:
//             $(this).transition("shake");
//             break;
//         case 3:
//             $(this).transition("pulse");
//             break;
//         case 4:
//             $(this).transition("bounce");
//             break;
//         default:
//             $(this).transition("jingle");
//     }
// })