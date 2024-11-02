
function updateURLParameter(url, param, paramVal)
{
    var TheAnchor = null;
    var newAdditionalURL = "";
    var tempArray = url.split("?");
    var baseURL = tempArray[0];
    var additionalURL = tempArray[1];
    var temp = "";

    if (additionalURL) 
    {
        var tmpAnchor = additionalURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor = tmpAnchor[1];
        if(TheAnchor)
            additionalURL = TheParams;

        tempArray = additionalURL.split("&");

        for (var i=0; i<tempArray.length; i++)
        {
            if(tempArray[i].split('=')[0] != param)
            {
                newAdditionalURL += temp + tempArray[i];
                temp = "&";
            }
        }        
    }
    else
    {
        var tmpAnchor = baseURL.split("#");
        var TheParams = tmpAnchor[0];
            TheAnchor  = tmpAnchor[1];

        if(TheParams)
            baseURL = TheParams;
    }

    if(TheAnchor)
        paramVal += "#" + TheAnchor;

    var rows_txt = temp + "" + param + "=" + paramVal;
    return baseURL + "?" + newAdditionalURL + rows_txt;
}
function reset_filter(){
    $('#filterForm').trigger("reset");
    $('#filterForm').find('.select2-hidden-accessible').val(null).trigger('change');
}$(window).on('pageshow', function(){
    $('#loading').hide();
});
$(document).ready(function(){
    $(".filter-form ").on("submit", function(){
        $('#loading').show();
    });
    $(".menu-item").on("click", function(){
        if (!$(this).hasClass("menu-accordion") && !$(this).hasClass("menu-perso")){
            $('#loading').show();
        }
    });//click
    $(".detail-link").on("click", function(){
        if (!$(this).hasClass("menu-accordion") && !$(this).hasClass("menu-perso")){
            $('#loading').show();
        }
    });//click
});//document ready

$(".dateinput").flatpickr({
    dateFormat: "d/m/Y",    
    "locale": "fr"
});
$(".mae-filter-form").find('input,textarea').addClass("form-control form-control-solid");
$(".mae-filter-form").find('select').addClass("form-select");
$(".date-range-picker").flatpickr({
    dateFormat: "d/m/Y",    
    locale: "fr",
    mode: "range",

});

function toggleFilterCard(){
    $("#filterCard").toggleClass('show');
    $('#filter_toggle_button_id').toggleClass('d-none');
    var width = window.innerWidth;
    if (width >= 1400){
        setCookie('filter_card_xxl_up', $("#filterCard").hasClass('show'), 1000);
    } else {
        setCookie('filter_card_xl_down', $("#filterCard").hasClass('show'), 1000);
    }
}


window.addEventListener("DOMContentLoaded", (e) => {
    $('select').on('select2:select', function (e) {
        $(this).closest('select').get(0).dispatchEvent(new Event('change'));
    });

});

// Function to set a cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}
// Function to get a cookie
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0){ 
            return c.substring(nameEQ.length, c.length);
        }
    }
    return null;
}

// Function to check the sidebar state on page load
document.addEventListener('DOMContentLoaded', (event) => {
    var sidebarState = getCookie('sidebar_minimize_state');
    var toggleElement = document.querySelector("#kt_app_sidebar_toggle");
    var toggle = KTToggle.getInstance(toggleElement);
    if (sidebarState === 'on') {
        toggle.toggle();
    } 

    var width = window.innerWidth;
    if (width >= 1400){
        var filterCardState = getCookie('filter_card_xxl_up');
        if (filterCardState === 'true') {
            $("#filterCard").addClass('show');
            $('#filter_toggle_button_id').addClass('d-none');
        }
    } else {
        var filterCardState = getCookie('filter_card_xl_down');
        if (filterCardState === 'true') {
            $("#filterCard").addClass('show');
            $('#filter_toggle_button_id').addClass('d-none');
        }
    }

});
