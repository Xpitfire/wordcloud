var clicked = false;

$(function () {
    $('form').on('submit', function () {
        if (!clicked) {
            $('#spinner').slideToggle('slow');
            clicked = true;
        }
    });
});