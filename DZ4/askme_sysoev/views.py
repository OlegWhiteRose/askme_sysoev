from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.db.models import Prefetch
from django.contrib.postgres.aggregates import ArrayAgg 
from django import conf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from askme_sysoev.models import *


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

    context = {
        'page': page,
        'visible_pages': visible_pages,
        'main_card': question_obj,
        'MEDIA_URL': conf.settings.MEDIA_URL,
    }

    return render(request, 'question.html', context)


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
