from django import forms
from ecopoints.models import UserProfile
from django.contrib.auth.models import User

#Two classes inheriting from forms.ModelForm
#They display required form fields for (1)base User class and (2)UserProfile model

class UserForm(forms.ModelForm):
    #Include this line to hide the password when rendering HTML form:
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
