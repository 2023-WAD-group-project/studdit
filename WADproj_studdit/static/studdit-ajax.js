$(document).ready(function() {
    $('#upvote').click(function() {
        var catecategoryIdVar;
        catecategoryIdVar = $(this).attr('data-categoryid');
    
        $.get('/rango/like_category/',
        {'category_id': catecategoryIdVar},
        function(data) {
            $('#votes').html(data);
            $('#like_btn').hide();
        })
    });
});

