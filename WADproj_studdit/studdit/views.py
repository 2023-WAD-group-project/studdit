from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from studdit.models import Post, Course, Student, Comment
from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from studdit.forms import PostForm, UserForm
# Create your views here.

@login_required
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
    comment = Comment.objects.filter(post=post).order_by('-date')
    votes = post.upvotes - post.downvotes
    if request.user.is_authenticated:
        username = request.user.id
    print(username)

    if post.upvoted_by.filter(id=username).exists():
        liked = "true"
        colourLiked = "btn btn-success"
    else:
        liked = "false"
        colourLiked = "btn btn-default"

    if post.downvoted_by.filter(id=username).exists():
        colourDisliked = "btn btn-danger"
        disliked = "true"
    else:
        colourDisliked = "btn btn-default"
        disliked = "false"
    
    print(liked)

    
    context_dict = {}
    context_dict['comment'] = comment
    context_dict['post'] = post
    context_dict['liked'] = liked
    context_dict['disliked'] = disliked
    context_dict['colourLiked'] = colourLiked
    context_dict['colourDisliked'] = colourDisliked

    context_dict['votes'] = votes
    
    
    return render(request, "post.html", context=context_dict)


@login_required
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



def login_page(request):
    context_dict = {}
    return render(request, "login.html", context=context_dict)

@login_required
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
            #return show_course(request, course_name_slug)
    else:
        print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'add_post.html', context_dict)

class LikePostView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.id
        
        post_id = request.GET['post_id']
        not_pressed = request.GET['not_pressed']
        
        

    
        
        
        
        try:
            post = Post.objects.get(id=str(post_id))
        except Post.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        
        print(username)
        if post.upvoted_by.filter(id=username).exists():
            
            post.upvoted_by.remove(request.user)
            post.upvotes = post.upvotes -1

        
        else:
            
            post.upvoted_by.add(request.user)
            
            if post.downvoted_by.filter(id=username).exists():
                print(post.downvoted_by.filter(id=username))
                post.downvoted_by.remove(request.user)
                post.downvotes = post.downvotes - 1
            
            
            post.upvotes = post.upvotes + 1

        
            

        post.save()
        
        return HttpResponse()
    
class DislikePostView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.id
        print("green")
        post_id = request.GET['post_id']
        not_pressed = request.GET['not_pressed']
        
        
        
        try:
            post = Post.objects.get(id=str(post_id))
        except Post.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        if post.downvoted_by.filter(id=username).exists():
            print("rry")
            
            post.downvoted_by.remove(request.user)
            post.downvotes = post.downvotes - 1

        
        else:
            
            post.downvoted_by.add(request.user)
            print("yellow")
            if post.upvoted_by.filter(id=username).exists():
                post.upvoted_by.remove(request.user)
                post.upvotes = post.upvotes -1
            
            
            post.downvotes = post.downvotes + 1

        
            

        post.save()
        return HttpResponse()
    
def user_login(request):
    print("huh")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            print(f"failed: {username}, {password}")
            return redirect(reverse("login") + "?failed_login")

        login(request, user)
        print(f"logged in: {username}, {password}")
        return redirect(reverse("profile"))


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

@login_required
def log_out(request):
    logout(request)
    return redirect(reverse("login"))