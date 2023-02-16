$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $(".tooltipped").tooltip();
    $(".collapsible").collapsible();
    $("select").formSelect();
    $(".datepicker").datepicker({
        format: "yyyy-mm-dd",
        disableWeekends: true,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});