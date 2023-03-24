from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from studdit.models import Post, Course, Student, Comment
from django.views import View
from django.contrib import messages
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from studdit.forms import PostForm, CourseForm, UserForm, CommentForm

import os
import re
regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@student.gla.ac.uk')
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
    #gets the post object
    post = Post.objects.get(course=Course.objects.get(code=course_name_slug), slug=slug)
    #get the comment objects and filter by date
    comment = Comment.objects.filter(post=post).order_by('-date')
    votes = post.upvotes - post.downvotes
    if request.user.is_authenticated:
        username = request.user.id
    print(username)
    #this logic here just determines whether the user has upvotes or downvoted the post and then makes sure that button are the appropriate colours.
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

            dest_folder = os.path.join(settings.MEDIA_ROOT, course_name_slug)

            try: os.mkdir(dest_folder)
            except FileExistsError: pass

            with open(os.path.join(dest_folder, post.filename), 'wb+') as f:
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
    return redirect(reverse('post', kwargs={'course_name_slug': course_name_slug, 'slug': post_slug}))

@login_required
def delete_post(request, course_code, post_slug):
    post = Post.objects.get(slug=post_slug)

    if post.post_author.user == request.user:
        print(f"deleting {post.title}")
        post.delete()
    else:
        print(f"did not delete {post.title}")
    return redirect(reverse("profile"))

class LikePostView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.id

        #fetch the data posted by ajax
        post_id = request.GET['post_id']
        not_pressed = request.GET['not_pressed']
        
        

    
        
        
        
        try:
            post = Post.objects.get(id=str(post_id))
        except Post.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        
        print(username)
        #this logic determines whether a user is upvoting or widthrawing their upvote from a post and then acts accordingly
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
        #fetch the data posted by ajax
        post_id = request.GET['post_id']
        not_pressed = request.GET['not_pressed']
        
        
        
        try:
            post = Post.objects.get(id=str(post_id))
        except Post.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        #this logic determines whether a user is downvoting or widthrawing their downvote from a post and then acts accordingly
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
            messages.error(request, 'Invalid username or password')
            return redirect(reverse("login") + "?failed_login")

        login(request, user)
        print(f"successful log in: {username}")
        return redirect(reverse("profile"))

def isValid(email):
    if re.fullmatch(regex, email):
      print("Valid email")
      return True
    else:
      print("Invalid email")
      return False
    
def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            print(user.email)
            if isValid(user.email):
                user.set_password(user.password)
                user.save()
                messages.success(request, 'Sign up successful!')

                student = Student.objects.get_or_create(user=user)

                login(request, user)
                print(f"successful log in: {user.username}")

                return redirect(reverse("profile"))
            messages.error(request, 'Invalid email - use a UofG email address.')

    return redirect(reverse("login"))




@login_required
def log_out(request):
    logout(request)
    return redirect(reverse("login"))

@login_required
def change_username(request):
    if request.method == 'POST':
        try:
            request.user.username = request.POST.get("username")
            request.user.save()
        except:
            pass


    return redirect(reverse('profile'))

@login_required
def change_password(request):
    
    if request.method == 'POST':
        if request.POST.get("newpass") == request.POST.get("newpass_confirm"):
            request.user.set_password(request.POST.get("newpass"))
            request.user.save()

    return redirect(reverse('profile'))

@login_required
def delete_account(request):
    request.user.delete()
    return redirect(reverse('login'))

@login_required
def request_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()

            return redirect(reverse('show_course', kwargs={'course_name_slug': course.code}))
        else:
            print("form errors:")
            print(form.errors)
    return redirect(request.META['HTTP_REFERER'])