from django import forms 
from studdit.models import Post ,Course, Student, Comment
from django.contrib.auth.models import User
from django.utils import timezone

class UserForm(forms.ModelForm):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)

class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=32)
    description = forms.CharField(max_length=1024*10)
    filename = forms.CharField(max_length=128, widget=forms.HiddenInput())
    file = forms.FileField()

    class Meta:
        model = Post
        fields = ("title", "description", "file", "filename")

class CourseForm(forms.ModelForm):

    code = forms.CharField(max_length=32)
    title = forms.CharField(max_length=1024*10)

    class Meta:
        model = Course
        fields = ("code", "title")


class CommentForm(forms.ModelForm):

    content = forms.CharField(max_length=1024*10)

    class Meta:
        model = Comment
        fields = ("content",)
