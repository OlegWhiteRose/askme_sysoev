from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
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


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags'] 
    
    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Title of your question here..',
                                                                                         'class': 'ms-5 w-50', 'name': 'title'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter content of your question here..', 'class': 'text',
                                                        'name': 'text'}), required=True)
    tags = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Put tags here..',
                                                                                        'name': 'tags', 'class': 'ms-5 w-50 mt-3'}))


class RegistrationForm(forms.Form):
    login = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your login here..', 'class': 'mt-5', 'name': 'login'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email here..', 'class': 'mt-4', 'name': 'email'})
    )
    nickname = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your nickname here..', 'class': 'mt-4', 'name': 'nickname'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password here..', 'class': 'mt-4', 'name': 'password'})
    )
    repeated_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password here..', 'class': 'mt-4', 'name': 'repeated-password'})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'name': 'avatar'})
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('Длина пароля должна быть >= 8 символам.')
        if not any(char.isalpha() for char in password):
            raise ValidationError('Пароль должен содержать хотя бы один символ.')
        return password


    def clean_repeated_password(self):
        password = self.cleaned_data.get('password')
        repeated_password = self.cleaned_data.get('repeated_password')
        if password != repeated_password:
            raise ValidationError('Пароли не совпадают.')
        return repeated_password


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже зарегистрирован.')
        return email
    
    def clean_login(self):
        login = self.cleaned_data.get('login')
        if User.objects.filter(username=login).exists():  
            raise ValidationError('Логин уже взят.')
        return login

