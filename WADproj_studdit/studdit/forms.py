from django import forms 
from studdit.models import Post ,Course

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
     
    class Meta:
        model = UserForm
        fields ('username', 'password', 'email',)
                               
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
                               
