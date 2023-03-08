$(document).ready(function() {
    
        
        
        
        
        pressed2 = false;
        pressed = false
        count = 5
        var votes = document.getElementById('votes').innerText
        parseInt(votes)



    $('#upvote').click(function() {
        
        
        
        var postIdVar;
        postIdVar = $(this).attr('data-postid');
        downvote.style.backgroundColor = ""
        if (pressed == false){
            if (pressed2 == true){
                votes ++
            }

            
            

            
            votes ++
        
        
    
          $.get('/like_post/',
          {'post_id': postIdVar, 'like_true': true},
          function(data) {
          $('#votes').html(votes);
          }
          )
          pressed = true
          
          upvote.style.backgroundColor = "green"
          //pressed1 = true
          

        }
        else{
            
            
            votes --
            pressed = false;

            
          
          
          

          $.get('/like_post/',
          {'post_id': postIdVar, 'like_true': false},
          function(data) {
          $('#votes').html(votes);
          }
          )
          upvote.style.backgroundColor = ""

          
          
          
        }
        pressed2 = false
        
        
        
        
        
    
        
            
            

            
            
    });
    

    $('#downvote').click(function() {
        
        
        var postIdVar;
        postIdVar = $(this).attr('data-postid');
        upvote.style.backgroundColor = ""
        if (pressed2 == false){
            pressed2 = true

            if (pressed == true){
                votes --
            }
            

            
            votes --
        
        
    
          $.get('/like_post/',
          {'post_id': postIdVar, 'like_true': true},
          function(data) {
          $('#votes').html(votes);
          }
          )
          
          
          downvote.style.backgroundColor = "red"
          //pressed1 = true
          

        }
        else{
            
            
            votes ++
            pressed2 = false;
          
          
          

          $.get('/like_post/',
          {'post_id': postIdVar, 'like_true': false},
          function(data) {
          $('#votes').html(votes);
          }
          )
          downvote.style.backgroundColor = ""

          
          
          
        }
        pressed = false
        
        
        
        
        
    
        
            
            

            
            
    });


    
});



    


