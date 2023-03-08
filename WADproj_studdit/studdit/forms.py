from django import forms 
from studdit.models import Post ,Course, Student
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
     
    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
                               
##need to add postForm
##agreed to leaving out courseForm as courses can be added manually (by admin)
