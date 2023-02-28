from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("homepage")

def course(request):
    raise Exception("NOT IMPLEMENTED")
    return HttpResponse("course page")

def post(request):
    raise Exception("NOT IMPLEMENTED")
    return HttpResponse("post page")

def login(request):
    return HttpResponse("login")

def profile(request):
    return HttpResponse("profile")
