$(document).ready(function() {

    $('#like_btn').click(function() {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');

    $.get('/ecopoints/like_category/',
        {'category_id': categoryIdVar},
        function(data) {
            $('#like_count').html(data);
            $('#like_btn').html('Liked');
        })
    });
});
