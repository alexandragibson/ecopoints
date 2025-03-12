//$(document).ready(function()) {

    hover_colour = '#62a162';

    $('a').hover(
        function() {
            $(this).css('color', hover_colour);
        },
        function() {
            $(this).css('color', 'white');
    });

    $('li').hover(
        function() {
            $(this).css('color', hover_colour);
        },
        function() {
            $(this).css('color', 'white');
    });

//});
