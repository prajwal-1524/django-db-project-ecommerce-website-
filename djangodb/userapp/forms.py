# userapp/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, Profile, vendor

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username',
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your password',
    }))


class UserSignUpForm(UserCreationForm):
    is_vendor = forms.BooleanField(required=False, label='Are you a vendor?', initial=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'is_vendor')

