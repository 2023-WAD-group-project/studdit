from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from studdit.models import Post, Course, Student, Comment
from django.views import View
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from studdit.forms import PostForm, UserForm, CommentForm

import os
# Create your views here.

@login_required
def home(request):
    context_dict = {}
    context_dict["courses"] = Course.objects.all()
    return render(request, "home.html", context=context_dict)

def test(request):
    context_dict = {}
    return render(request, "test.html", context=context_dict)

@login_required
def post(request, course_name_slug, slug):
    post = Post.objects.get(course=Course.objects.get(code=course_name_slug), slug=slug)
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

@login_required
def add_post(request, course_name_slug):
    try:
        course = Course.objects.get(code=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None:
        return redirect(reverse('home'))

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

    if form.is_valid():
        if course:
            post = form.save(commit=False)
            post.course = course
            post.post_author = Student.objects.get(user=request.user)
            post.views = 0
            post.save()

            with open(os.path.join(settings.MEDIA_ROOT, course_name_slug, post.filename), 'wb+') as f:
                for chunk in request.FILES["file"].chunks():
                    f.write(chunk)

            return redirect(reverse('show_course', kwargs={'course_name_slug': course_name_slug}))
    else:
        print("form errors:")
        print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'add_post.html', context=context_dict)

@login_required
def add_comment(request, course_name_slug, post_slug):
    try:
        course = Course.objects.get(code=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None:
        return redirect(reverse('home'))

    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        post = None

    if course is None:
        return redirect(reverse('home'))
    if post is None:
        return redirect(reverse('home'))


    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)

    if form.is_valid():
        if course:
            comment = form.save(commit=False)
            comment.course = course
            comment.post = post
            comment.student = Student.objects.get(user=request.user)
            comment.save()

            return redirect(reverse('post', kwargs={'course_name_slug': course_name_slug, 'slug': post_slug}))
    else:
        print("form errors:")
        print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'add_post.html', context=context_dict)

@login_required
def delete_post(request, course_code, post_slug):
    post = Post.objects.get(slug=post_slug)

    if post.post_author.user == request.user:
        print(f"deleting {post.title}")
        post.delete()
    else:
        print(f"did not delete {post.title}")
    return HttpResponse("something")

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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            print(f"failed log in: {username}")
            return redirect(reverse("login") + "?failed_login")

        login(request, user)
        print(f"successful log in: {username}")
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


class CommentPost(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user

        
        post_id = request.GET['post_id']
        post = Post.objects.get(id=str(post_id))
        content = request.GET['content']
        print(post_id.__class__)
        print(content)
        new = Comment(post=post,student=username, content = content)
        new.save()
        
        
        
        
        
        
        
        return HttpResponse()

