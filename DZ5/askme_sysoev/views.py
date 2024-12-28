from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from django.db.models import Prefetch
from django.contrib.postgres.aggregates import ArrayAgg 
from django.contrib.auth import authenticate, login as auth_login
from django import conf
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from askme_sysoev.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from .models import Image  


def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        print("In image")
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = form.save()
            
            return JsonResponse({'success': True, 'file_url': image.file.url})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'No file uploaded'})


def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get('page', 1) 
    paginator = Paginator(objects_list, per_page)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page


def find_visible_pages(page):
    visible_pages = []
    page_range = page.paginator.page_range
    current_page = page.number
    for num in page_range:
        if num == 1 or num == page.paginator.num_pages or (num >= current_page - 2 and num <= current_page + 2):
            visible_pages.append(num)
        elif num == current_page - 3 or num == current_page + 3:
            visible_pages.append('...')

    return visible_pages


def index(request):
    question_tags = Prefetch('questiontag', queryset=QuestionTag.objects.select_related('tag'))
    questions = Question.objects.newest().prefetch_related(question_tags).annotate(
        tags=ArrayAgg('questiontag__tag__name', distinct=True), 
        answers_cnt=Count('answer', distinct=True)
    )

    cards = questions.values(
        'id', 'title', 'text', 'rating', 'created_at', 'created_user', 'answers_cnt', 'tags', 'created_user__profile__avatar'
    )

    page = paginate(cards, request, per_page=10)
    visible_pages = find_visible_pages(page)

    context = {
        'page': page,
        'visible_pages': visible_pages,
        'MEDIA_URL': conf.settings.MEDIA_URL,
    }

    return render(request, 'index.html', context)


@login_required
def ask(request):
    if request.user.is_authenticated and request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_user = request.user 
            question.save()

            tags = request.POST.get('tags')
            if tags:
                tag_names = [tag.strip() for tag in tags.split(',')] 
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    QuestionTag.objects.create(question=question, tag=tag)

            return redirect('question', id=question.id)  
        else:
            context = {
                'form': form,
                'errors': form.errors, 
            }
            return render(request, 'ask.html', context)
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})


def question(request, id):
    question_tags = Prefetch('questiontag', queryset=QuestionTag.objects.select_related('tag'))

    question_obj = get_object_or_404(
        Question.objects.prefetch_related(question_tags).annotate(
            tags=ArrayAgg('questiontag__tag__name', distinct=True)
        ).values(
            'id', 'title', 'text', 'rating', 'created_user__username', 'created_user__profile__avatar', 'tags'
        ), id=id
    )

    cards = Answer.objects.filter(question__id=id).select_related('created_user__profile').values(
        'id', 'text', 'rating', 'created_user__username', 'created_user__profile__avatar'
    ).order_by('-rating')

    page = paginate(cards, request, per_page=3)
    visible_pages = find_visible_pages(page)

    if request.user.is_authenticated and request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = get_object_or_404(Question, id=id)
            answer.created_user = request.user  
            answer.save()
            return redirect('question', id=id) 
    else:
        form = AnswerForm()


    context = {
        'page': page,
        'visible_pages': visible_pages,
        'main_card': question_obj,
        'MEDIA_URL': conf.settings.MEDIA_URL,
        'form': form,
    }

    return render(request, 'question.html', context)


@login_required
def settings(request):
    user = request.user
    profile = user.profile
    context = {
        'MEDIA_URL': conf.settings.MEDIA_URL,
    }

    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, initial={'current_user': user})

        if form.is_valid():
            with transaction.atomic():
                login = form.cleaned_data.get('login')
                email = form.cleaned_data.get('email')
                nickname = form.cleaned_data.get('nickname')

                if login != user.username:
                    user.username = login
                if email != user.email:
                    user.email = email
                if nickname != profile.nickname:
                    profile.nickname = nickname

                user.save()
                profile.save()

                if 'avatar' in request.FILES:
                    avatar_file = request.FILES['avatar']
                    image = Image.objects.create(name=f"{user.username}_avatar", file=avatar_file)
                    profile.avatar = image.file

                    profile.save()

                return redirect('settings')  

    else:
        form = SettingsForm(initial={'current_user': user, 'login': user.username, 'email': user.email, 'nickname': profile.nickname})

    context['form'] = form
    return render(request, 'settings.html', context)


def register(request):
    context = {}

    if not request.user.is_authenticated and request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)

        if form.is_valid():
            print("In reg")
            with transaction.atomic():  
                user = User.objects.create_user(
                    username=form.cleaned_data['login'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )

                profile = Profile.objects.create(user=user)

                if 'avatar' in request.FILES:
                    avatar_file = request.FILES['avatar']
                    image = Image.objects.create(name=f"{user.username}_avatar", file=avatar_file)
                    profile.avatar = image.file  
                    profile.save()

            user = authenticate(username=form.cleaned_data['login'], password=form.cleaned_data['password'])
            auth_login(request, user)
            return redirect('index')  
        else:
            context['errors'] = form.errors 
    else:
        form = RegistrationForm()

    context['form'] = form
    return render(request, 'register.html', context)


def login(request):
    context = {'errors': []}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index') 
            else:
                context['errors'].append('Неправильный логин или пароль')
        else:
            context['errors'].extend(form.errors.values())
    else:
        form = LoginForm()

    context['form'] = form
    return render(request, 'login.html', context)



def hot(request):
    question_tags = Prefetch('questiontag', queryset=QuestionTag.objects.select_related('tag'))
    questions = Question.objects.best().prefetch_related(question_tags).annotate(
        tags=ArrayAgg('questiontag__tag__name', distinct=True), 
        answers_cnt=Count('answer', distinct=True)  
    )

    cards = questions.values(
        'id', 'title', 'text', 'rating', 'created_at', 'created_user', 'answers_cnt', 'tags', 'created_user__profile__avatar'
    )

    page = paginate(cards, request, per_page=10)
    visible_pages = find_visible_pages(page)

    context = {
        'page': page,
        'visible_pages': visible_pages,
        'MEDIA_URL': conf.settings.MEDIA_URL,
    }

    return render(request, 'hot.html', context)


def tag(request, name):
    tag_obj = get_object_or_404(Tag, name=name)
    question_tags = Prefetch('questiontag', queryset=QuestionTag.objects.select_related('tag'))

    questions = Question.objects.newest().prefetch_related(question_tags).annotate(
        tags=ArrayAgg('questiontag__tag__name', distinct=True), 
        answers_cnt=Count('answer')
    ).filter(questiontag__tag=tag_obj)

    cards = questions.values(
        'id', 'title', 'text', 'rating', 'created_at', 'created_user', 'answers_cnt', 'tags', 'created_user__profile__avatar'
    )

    page = paginate(cards, request, per_page=10)
    visible_pages = find_visible_pages(page)

    context = {
        'page': page,
        'visible_pages': visible_pages,
        'tag': name,
        'MEDIA_URL': conf.settings.MEDIA_URL,
    }

    return render(request, 'tag.html', context)
