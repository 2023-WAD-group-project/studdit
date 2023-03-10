$(document).ready(function() {
    
        
        
        
        
        pressed2 = false;
        pressed = false
        count = 5
        var votes = document.getElementById('votes').innerText
        parseInt(votes)



    $('#upvote').click(function() {
        
        
        
        var postIdVar;
        postIdVar = $(this).attr('data-postid');
        postUserVar = $(this).attr('data-username');
        postUserLiked = $(this).attr('data-liked');

        downvote.style.backgroundColor = ""
        
        
        if (pressed == false){
          alert(postUserLiked)
          
            if (pressed2 == true){
              if (postUserLiked == "false"){
                votes ++
              }
              else{
                alert("erer")
                votes = votes - 1
              }
            }

            
            

            if (postUserLiked == "false"){
              
              votes ++

            }
            
           
            
        
        
    
          $.get('/like_post/',
          {'post_id': postIdVar, 'not_pressed': true, 'username': postUserVar},
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
          {'post_id': postIdVar, 'not_pressed': false, 'username': postUserVar},
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
        postUserVar = $(this).attr('data-username');
        postUserDisliked = $(this).attr('data-disliked');
        upvote.style.backgroundColor = ""
        
        if (pressed2 == false){
          
            pressed2 = true

            if (pressed == true){
              if (postUserDisliked == "false"){
                votes --
              }
            }
            

            if (postUserDisliked == "false"){
            votes --
            }
            alert(postUserDisliked)
        
        
    
          $.get('/dislike_post/',
          {'post_id': postIdVar, 'not_pressed': true, 'username': postUserVar},
          function(data) {
          $('#votes').html(votes);
          }
          )
          
          
          downvote.style.backgroundColor = "red"
          
          

        }
        else{
            
            
            votes ++
            pressed2 = false;
            
          
          
          

          $.get('/dislike_post/',
          {'post_id': postIdVar, 'not_pressed': false, 'username': postUserVar},
          function(data) {
          $('#votes').html(votes);
          }
          )
          downvote.style.backgroundColor = ""

          
          
          
        }
        pressed = false
        
        
        
        
        
    
        
            
            

            
            
    });
    


    
});



    


