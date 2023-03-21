$(document).ready(function() {
  upvotePressed = false
  downvotePressed2 = false
    
        
        
        
        
        pressed2 = false;
        pressed = false
        count = 5
        var votes = document.getElementById('votes').innerText
        parseInt(votes)



    $('#upvote').click(function() {
      downvote.style.backgroundColor = "grey"
        
        
        
        var postIdVar;
        postIdVar = $(this).attr('data-postid');
        postUserVar = $(this).attr('data-username');
        if (upvotePressed == false){
          postUserLiked = $(this).attr('data-liked');

        }
        else{
          postUserLiked = "false"

        }
        if (downvotePressed2 == false){
          postUserDisliked = $(downvote).attr('data-disliked');

        }
        else{
          postUserDisliked = "false"

        }
        

        downvote.class = "btn btn-default"
        
        
        if (pressed == false){
          upvote.style.backgroundColor = "green"
          
          pressed = true
          
          
          
          
          
            if (pressed2 == true || postUserDisliked == "true"){
              

                votes ++
              
              
            }

            
            

            if (postUserLiked == "false"){
              
              votes ++

            }
            else{
              upvote.style.backgroundColor = "grey"
              
              if (upvotePressed == false){
                
                votes =votes -1
                upvotePressed = true
                pressed = false
                

                
  
              }

            }

            
            
            
            
           
            
        
        
    
          $.get('/like_post/',
          {'post_id': postIdVar, 'not_pressed': true, 'username': postUserVar},
          function(data) {
          $('#votes').html(votes);
          }
          )
          
          
          
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
          upvote.style.backgroundColor = "grey"
          

          
          
          
        }
        pressed2 = false
        
        
        
        
        
    
        
            
            

            
            
    });
    

    $('#downvote').click(function() {
        
        
        var postIdVar;
        postIdVar = $(this).attr('data-postid');
        postUserVar = $(this).attr('data-username');
        if (downvotePressed2 == false){
          postUserDisliked = $(this).attr('data-disliked');

        }
        else{
          postUserDisliked = "false"

        }

        if (upvotePressed == false){
          postUserLiked = $(upvote).attr('data-liked');

        }
        else{
          postUserLiked = "false"

        }
        upvote.style.backgroundColor = "grey"
        
        if (pressed2 == false){
          downvote.style.backgroundColor = "red"
          
          
          
            pressed2 = true

            if (pressed == true || postUserLiked == "true"){
                
                votes --
              
            }
            

            if (postUserDisliked == "false"){
            votes --
            }
            else{
              downvote.style.backgroundColor = "grey"
              
              if (downvotePressed2 == false){
                
                
                votes ++
                downvotePressed2 = true
                pressed2 = false
                
                
  
              }

            }

            
            
        
        
    
          $.get('/dislike_post/',
          {'post_id': postIdVar, 'not_pressed': true, 'username': postUserVar},
          function(data) {
          $('#votes').html(votes);
          }
          )
          
          
          
          
          

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
          downvote.style.backgroundColor = "grey"

          
          
          
        }
        pressed = false
        
        
        
        
        
    
        
            
            

            
            
    });

    $('#comment').click(function() {
      postIdVar = $(this).attr('data-postid');
      postUserVar = $(this).attr('data-username');
      alert("ffhhs")
      
      let html = document.getElementById("site-search").value;
      
      document.getElementById("site-search").value = ""

      $.get('/comment/',
          {'post_id': postIdVar, 'content': html},
          function(data) {
          
          }
          )
      //location.reload();
      return false;

    
    });
    


    
});



    


