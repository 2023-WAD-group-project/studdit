from django.http import HttpResponse
from django.shortcuts import render
from studdit.models import Post, Course
from django.views import View

# Create your views here.

def home(request):
    context_dict = {}
    context_dict["courses"] = Course.objects.all()
    return render(request, "home.html", context=context_dict)

def test(request):
    context_dict = {}
    return render(request, "test.html", context=context_dict)


def course(request):
    # note that this view wont be fully completed until we set up the database,
    # so worry about the other views for now
    #raise Exception("NOT IMPLEMENTED")

    context_dict = {}
    return render(request, "course.html", context=context_dict)

def post(request, slug):
    post = Post.objects.get(slug=slug)

    
    context_dict = {}
    context_dict['post'] = post
    
    
    return render(request, "post.html", context=context_dict)

def login(request):
    context_dict = {}
    return render(request, "login.html", context=context_dict)

def profile(request):
    context_dict = {}
    return render(request, "profile.html", context=context_dict)


def show_course(request, course_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(slug=course_name_slug)
        post = Post.objects.filter(course=course)
        context_dict['posts'] = post
        context_dict['course'] = course
    except Course.DoesNotExist:
        context_dict['course'] = None
        context_dict['posts'] = None
    return render(request, 'course.html', context=context_dict)

def add_post(request, course_name_slug):
    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None:
        return redirect(reverse('home'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

    if form.is_valid():
        if category:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

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
    

