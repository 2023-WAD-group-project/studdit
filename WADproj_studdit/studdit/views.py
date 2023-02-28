from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    context_dict = {}
    return render(request, "home.html", context=context_dict)

def course(request):
    # note that this view wont be fully completed until we set up the database,
    # so worry about the other views for now
    raise Exception("NOT IMPLEMENTED")

    context_dict = {}
    return render(request, "course.html", context=context_dict)

def post(request):
    # note that this view wont be fully completed until we set up the database,
    # so worry about the other views for now
    raise Exception("NOT IMPLEMENTED")

    context_dict = {}
    return render(request, "post.html", context=context_dict)

def login(request):
    context_dict = {}
    return render(request, "login.html", context=context_dict)

def profile(request):
    context_dict = {}
    return render(request, "profile.html", context=context_dict)
