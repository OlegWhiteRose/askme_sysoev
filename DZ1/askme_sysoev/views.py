# views.py
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def ask(request):
    context = {
        'errors': []
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        tags = request.POST.get('tags')

        # Для примера
        if not title:
            context['errors'].append('Sorry, there is no title!')
        if not text:
            context['errors'].append('Sorry, there is no text!')
        if not tags:
            context['errors'].append('Sorry, there is no tags!')

    return render(request, 'ask.html', context)



def question(request):
    return render(request, 'question.html')


def settings(request):
    return render(request, 'settings.html')


def register(request):
    context = {
        'errors': []
    }

    if request.method == 'POST':
        email = request.POST.get('email')

        rules = (
            email and 
            isinstance(email, str)
        )
        if rules:
            if email.strip() == 'dr.pepper@mail.ru': # Для примера
                context['errors'].append('Sorry, this email address already registered!')

    return render(request, 'register.html', context)


def login(request):
    context = {
        'errors': []
    }

    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        rules = (
            login and password and 
            isinstance(login, str) and
            isinstance(password, str)
        )
        if rules:
            if password != '1234': # Для примера
                context['errors'].append('Sorry, wrong password!')

    return render(request, 'login.html', context)
