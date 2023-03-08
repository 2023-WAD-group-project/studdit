from django.http import HttpResponse
from studdit.models import Course
from django.core import serializers
import json
"""
endpoint docs:
arguments:
show_non_zero - will we include courses with no posts?
title_contains - we should only return courses which have this string in the title.
"""

def get_courses(request):
    arguments = request.GET

    courses = Course.objects.filter(title__contains=arguments.get("title", ""))

    if arguments.get("showempty", "false")!="true":
        courses = courses.filter(post__isnull=False)

    response = json.dumps([course for course in courses.values()])
    # response = serializers.serialize('json', courses) # alternative method to serialize the json
    return HttpResponse(response);