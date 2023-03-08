from django.http import HttpResponse
from django.shortcuts import render
from studdit.models import Course

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
        courses = courses.filter(post__isnull=False)


    if arguments.get("format", "json") == "json":
        response = json.dumps([course for course in courses.values()])
        # response = serializers.serialize('json', courses) # alternative method to serialize the json
        return HttpResponse(response);
    elif arguments.get("format", "json") == "xml":
        context_dict = {}
        context_dict["courses"] = courses
        context_dict["settings"] = dict(arguments).get("xml_fields[]", "title")
        return render(request, 'course_card.html', context=context_dict)