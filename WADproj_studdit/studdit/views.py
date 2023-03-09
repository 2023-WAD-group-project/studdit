from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from studdit.models import Post, Course, Student
from django.views import View

from studdit.forms import UserForm
# Create your views here.

def home(request):
    context_dict = {}
    context_dict["courses"] = Course.objects.all()
    return render(request, "home.html", context=context_dict)

def test(request):
    context_dict = {}
    return render(request, "test.html", context=context_dict)

def show_course(request, course_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(code=course_name_slug)
        post = Post.objects.filter(course=course)
        context_dict['posts'] = post
        context_dict['course'] = course
    except Course.DoesNotExist:
        context_dict['course'] = None
        context_dict['posts'] = None
    return render(request, 'course.html', context=context_dict)

def post(request):
    context_dict = {}
    return render(request, "post.html", context=context_dict)

def login(request):
    context_dict = {}
    return render(request, "login.html", context=context_dict)

def profile(request):
    context_dict = {}
    return render(request, "profile.html", context=context_dict)


def add_post(request, course_name_slug):
    try:
        course = Course.objects.get(code=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None:
        return redirect(reverse('home'))

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

    if form.is_valid():
        if course:
            post = form.save(commit=False)
            post.course = course
            post.views = 0
            post.save()

            return redirect(reverse('show_course', kwargs={'course_name_slug': course_name_slug}))
    else:
        print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'post.html', context=context_dict)

class LikePostView(View):
    def get(self, request):
        print("yellow")
        post_id = request.GET['post_id']
        like_true = request.GET['like_true']
        
        
        try:
            post = Post.objects.get(id=str(post_id))
        except Post.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        return HttpResponse()
    

def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            student = Student.objects.get_or_create(user=user)

            return redirect(reverse("profile"))
    return redirect(reverse("login"))