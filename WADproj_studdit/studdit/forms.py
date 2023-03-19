from django import forms 
from studdit.models import Post ,Course, Student, Comment
from django.contrib.auth.models import User
from django.utils import timezone

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
     
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
                               

# agreed to leaving out courseForm as courses can be added manually (by admin)
class PostForm(forms.ModelForm):

    # i also feel like there should be a something declaring what
    # student the post belongs to
    #post_author = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    title = forms.CharField(max_length=32)
    description = forms.CharField(max_length=1024*10)
    #filename = forms.CharField(max_length=128, widget=forms.HiddenInput())
    file = forms.FileField()

    #slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    # wasnt sure what other fields to include, dont know if 
    # necessary to include upvoted_by or downvoted_by and not 

    class Meta:
        model = Post
        #fields = ("course", "title", "description", "filename", "file", "slug")
        exclude = ("post_author", "upvoted_by", "downvoted_by", "course")
        fields = ("title", "description", "file", "filename")
    


