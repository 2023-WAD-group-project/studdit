function searchAndUpdateCourses(searchStr)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()
    {
        if (this.readyState == 4 && this.status == 200)
        { document.getElementById("courses_div").innerHTML = this.responseText; }
    };
    xhttp.open("GET", "get_courses?title=" + searchStr + "&showempty=true&format=xml&xml_fields[]=title&xml_fields[]=code&xml_fields[]=exis_mate&xml_fields[]=likes", true);
    xhttp.send();
}

$("#posts_div").ready(function() {
    searchAndUpdateCourses("")
});