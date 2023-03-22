$("#posts_div").ready(function() {

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function()
    {
        if (this.readyState == 4 && this.status == 200)
        { document.getElementById("posts_div").innerHTML = this.responseText; }
    };

    var template_data = document.getElementById("template_data")
    var get_posts_url = template_data.getAttribute("data-get_posts_url")
    var user_username = template_data.getAttribute("data-user_username")
    xhttp.open("GET", get_posts_url + "?format=xml&student=" + user_username + "&xml_fields[]=votes&xml_fields[]=delete", true);
    xhttp.send();

});