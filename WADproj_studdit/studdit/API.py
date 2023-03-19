from django.http import HttpResponse
from django.shortcuts import render
from studdit.models import Course, Post
from datetime import datetime

# from django.core import serializers
import json

"""
endpoint docs:
arguments:
showempty - will we include courses with no posts? true/false (default is false)
title - we should only return courses which have this string in the title. (default is all courses)
format - json or xml? (default is json)
"""
def get_courses(request):
    arguments = request.GET
    print(arguments)

    courses = Course.objects.filter(title__contains=arguments.get("title", ""))

    if arguments.get("showempty", "false") != "true":
        courses = set(courses.filter(post__isnull=False))

    if arguments.get("format", "json") == "json":
        response = json.dumps([course for course in courses.values()])
        # response = serializers.serialize('json', courses) # alternative method to serialize the json
        return HttpResponse(response);
    elif arguments.get("format", "json") == "xml":
        context_dict = {}
        context_dict["courses"] = courses
        context_dict["settings"] = dict(arguments).get("xml_fields[]", "title")
        return render(request, 'course_card.html', context=context_dict)

"""
endpoint docs:
arguments:
course - if this is specified, we filter the returnable to only include the posts associated with this course.
student - if this is specified, we filter the returnable to only include posts created by the student with the specified username.
title - if this is specified, we filter the returnable to only include posts containing the specififed string in the title.
format - json or xml. if xml, we return a rendered template containing html to display the posts on a webpage.
"""
def json_fallback(obj):
    if isinstance(obj, datetime):
        return obj.timestamp() # alternatively could use .isoformat() in future if need to change to printable date
    raise TypeError ("Type %s not serializable" % type(obj))
def get_posts(request):
    arguments = request.GET
    print(arguments)

    posts = Post.objects.all()
    posts_courseFiltered = posts
    posts_userFiltered = posts

    if "student" in arguments:
        posts = posts.filter(post_author__user__username__exact=arguments["student"])

    if "course" in arguments:
        posts = posts.filter(course_id__exact=arguments["course"])

    if "title" in arguments:
        posts = posts.filter(title__contains=arguments["title"])


    if arguments.get("format", "json") == "json":
        response = json.dumps([post for post in posts.values()], default=json_fallback)
        return HttpResponse(response);
    elif arguments.get("format", "json") == "xml":
        context_dict = {}
        context_dict["posts"] = posts
        context_dict["settings"] = dict(arguments).get("xml_fields[]", "title")
        return render(request, 'post_card.html', context=context_dict)
