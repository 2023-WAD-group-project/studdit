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

# agreed to leaving out courseForm as courses can be added manually (by admin)
class PostForm(forms.ModelForm):

    title = forms.CharField(max_length=32)
    description = forms.CharField(max_length=1024*10)
    filename = forms.CharField(max_length=128, widget=forms.HiddenInput())
    file = forms.FileField()

    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # wasnt sure what other fields to include, dont know if 
    # necessary to include upvoted_by or downvoted_by and not 

    class Meta:
        model = Post
        fields = ("title", "description", "file", "filename")


class CommentForm(forms.ModelForm):

    content = forms.CharField(max_length=1024*10)

    class Meta:
        model = Comment
        fields = ("content",)
