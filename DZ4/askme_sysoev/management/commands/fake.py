import os
import random, string
from datetime import datetime, timedelta
from django.db import transaction
from django.contrib.auth.models import User
from askme_sysoev.models import Profile, Question, Answer, Tag, QuestionTag


class FakeUsers:
    def __init__(self, ratio, command):
        self.command = command
        self.__call__(ratio)


    def __call__(self, ratio):        
        # На всякий, чтобы откатилось, если вдруг что-то пошло не так
        with transaction.atomic():
            self.create_users(ratio)
            self.create_tags(ratio)
            self.create_questions(ratio * 10)


    def get_avatar_files(self):
        uploads_dir = 'uploads' 
        avatar_files = [
            f for f in os.listdir(uploads_dir) 
            if f.lower().endswith(('.jpg', '.png'))
        ]
        return avatar_files


    def gen_random_string(self):
        length = random.randint(5, 30)
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))


    def create_users(self, ratio):
        User.objects.all().delete()
        Profile.objects.all().delete()

        avatar_files = self.get_avatar_files()

        usernames = set()
        users = []
        profiles = []
        for _ in range(ratio):
            username = self.gen_random_string()
            while username in usernames:
                username = self.gen_random_string()

            email = username + '@mail.ru'
            password = 'test'

            user = User(
                username=username,
                email=email,
                password=password
            )

            users.append(user)

            profiles.append(Profile(
                user=user,
                avatar=random.choice(avatar_files),  
                nickname=username,
            ))


        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)

        self.command.stdout.write(self.command.style.SUCCESS(f'{len(users)} Users and profiles successfully created!'))     

        return users


    def create_tags(self, ratio):
        Tag.objects.all().delete()

        tags = []
        names = set()
        for _ in range(ratio):
            name = self.gen_random_string()
            if name in names:
                continue
            else:
                names.add(name)
            
            tag = Tag(name=name)
            tags.append(tag)


        Tag.objects.bulk_create(tags)

        self.command.stdout.write(self.command.style.SUCCESS(f'{len(tags)} Tags successfully created!'))   


    def gen_random_date(self):
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2023, 12, 31)
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)


    def create_questions(self, ratio):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        QuestionTag.objects.all().delete()

        tags = list(Tag.objects.all())
        users = User.objects.all()

        questoins_cnt = ratio
        # answers_cnt = ratio * 10

        questions = []
        questions_tags = []
        answers = []
        for _ in range(questoins_cnt):
            question = Question(
                created_user=random.choice(users),
                title=self.gen_random_string()+ '?',
                rating=random.randint(0, 1000),
                text=self.gen_random_string(),
                created_at=self.gen_random_date(),
            )

            questions.append(question)

            random_tags = random.sample(tags, k=4)
            for tag in random_tags:
                question_tag = QuestionTag(
                    tag=tag,
                    question=question,
                )
                questions_tags.append(question_tag)

            for _ in range(10):
                answer = Answer(
                    created_user=random.choice(users),
                    rating=random.randint(0, 200),
                    text=self.gen_random_string(),
                    question=question,
                )
                answers.append(answer)
        
        Question.objects.bulk_create(questions)
        Answer.objects.bulk_create(answers)
        QuestionTag.objects.bulk_create(questions_tags)

        self.command.stdout.write(self.command.style.SUCCESS(f'{len(questions)} questions successfully created!'))
