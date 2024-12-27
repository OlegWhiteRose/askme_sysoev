from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

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

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']  

    text = forms.CharField(widget=forms.Textarea(attrs={'id': 'comment', 'class': 'comment', 'placeholder': 'Enter your answer here..'}))