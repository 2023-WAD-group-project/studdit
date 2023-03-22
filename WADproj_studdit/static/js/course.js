var template_data = document.getElementById("template_data")
var get_posts_url = template_data.getAttribute("data-get_posts_url")
var course_code = template_data.getAttribute("data-course_code")

function searchAndUpdatePosts(searchStr)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()
    {
        if (this.readyState == 4 && this.status == 200)
        { document.getElementById("posts_div").innerHTML = this.responseText; }
    };
    xhttp.open("GET", get_posts_url + "?title=" + searchStr + "&format=xml&course=" + course_code + "&xml_fields[]=votes", true);
    xhttp.send();
}

$("#posts_div").ready(function() { searchAndUpdatePosts("") });