$(document).ready(function() {
    $('#upvote').click(function() {
        var postIdVar;
        postIdVar = $(this).attr('data-postid');
    
        $.get('/rango/like_post/',
        {'post_id': postIdVar},
        function(data) {
            $('#votes').html(data);
            $('#upvote').hide();
        })
    });
});

