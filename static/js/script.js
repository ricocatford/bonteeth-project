$(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $(".tooltipped").tooltip();
    $(".collapsible").collapsible();
    $("select").formSelect();
    $(".datepicker").datepicker({
        format: "yyyy-mm-dd",
        yearRange: 1,
        disableWeekends: true,
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
    $(".timepicker").timepicker({
        defaultTime: "09:00",
    });
});

