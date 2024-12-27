from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'mt-5',
            'placeholder': 'Enter your login here',
            'name': 'login'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'mt-4',
            'placeholder': 'Enter your password here',
            'name': 'password'
        })
    )
    