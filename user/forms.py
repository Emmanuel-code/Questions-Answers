from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UpdateProfileForm(forms.ModelForm):
    username=forms.CharField(max_length=50)

    class Meta:
        model=Profile
        fields=('username', 'first_name', 'last_name', 'email','image','bio')


class SignUpForm(UserCreationForm):
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    username=forms.CharField(max_length=150)
    email=forms.EmailField(max_length=200)

    class Meta:
        model=User
        fields=('username', 'first_name', 'last_name', 'email','password1','password2')

#
# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model=Profile
#         fields=['user', 'image', 'email']