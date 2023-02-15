$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $(".tooltipped").tooltip();
    $(".collapsible").collapsible();
    $(".datepicker").datepicker({
        format: "yyyy-mm-dd",
        disableWeekends: true,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
});