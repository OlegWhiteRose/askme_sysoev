import os
import random, json, csv
from django.db import transaction
from django.contrib.auth.models import User
from askme_sysoev.models import Profile, Question, Answer, Tag, QuestionTag

from concurrent.futures import ThreadPoolExecutor

class RealUsers:
    def __init__(self, ratio, command):
        self.command = command
        self.__call__(ratio)


    def __call__(self, ratio):
        data = None
        dataset_path = 'data/dataset/parse.jsonl'
        if dataset_path:
            self.command.stdout.write(self.command.style.SQL_TABLE(f'Using dataset file: {dataset_path}'))
            with open(dataset_path, 'r', encoding='utf-8') as f:
                data = [json.loads(line) for line in f]
        else:
            self.command.stdout.write(self.command.style.ERROR(f'Dataset file not found'))

        if data is not None:
            self.command.stdout.write(self.command.style.SUCCESS(f'Dataset successfully loaded!'))
        else:
            return
        
        # На всякий, чтобы откатилось, если вдруг что-то пошло не так
        with transaction.atomic():
            self.create_users(data, ratio)
            self.create_tags(data, ratio)
            self.create_questions(data, ratio * 10)
        
        
    def get_avatar_files(self):
        uploads_dir = 'uploads' 
        avatar_files = [
            f for f in os.listdir(uploads_dir) 
            if f.lower().endswith(('.jpg', '.png'))
        ]
        return avatar_files
    

    def create_users(self, data, ratio):
        User.objects.all().delete()
        Profile.objects.all().delete()

        avatar_files = self.get_avatar_files()

        usernames = set()
        users = []
        profiles = []
        for line in data:
            username = line['question_author_name']
            
            i = 1
            while True:
                email = username + '@mail.ru'
                password = 'test'

                if username in usernames:
                    if f'answer_{i}' not in line['answers']:
                        break

                    username = line['answers'][f'answer_{i}']['answer_author_name']
                    i += 1
                    continue
                else:
                    usernames.add(username)

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

                if f'answer_{i}' not in line['answers']:
                    break

                username = line['answers'][f'answer_{i}']['answer_author_name']
                i += 1


        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        
        if len(users) < ratio:
            self.command.stdout.write(self.command.style.ERROR('Not enough users and profiles!'))     
            return

        self.command.stdout.write(self.command.style.SUCCESS(f'{len(users)} Users and profiles successfully created!'))     

        return users


    def create_tags(self, data, ratio):
        Tag.objects.all().delete()
        
        tags = []
        names = set()
        for line in data:
            name = line['question_category']
            if name in names:
                continue
            else:
                names.add(name)
            
            tag = Tag(name=name)
            tags.append(tag)

        additional_data = []
        with open('data/dataset/words.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) 
            for row in csv_reader:
                additional_data.append(row)
        
        for line in additional_data:
            name = line['CORRECT;MISTAKE;WEIGHT'].split(';')[0]
            if name in names:
                continue
            else:
                names.add(name)
            
            tag = Tag(name=name)
            tags.append(tag)

        Tag.objects.bulk_create(tags)

        if len(tags) < ratio:
            self.command.stdout.write(self.command.style.ERROR('Not enough tags!'))     
            return

        self.command.stdout.write(self.command.style.SUCCESS(f'{len(tags)} Tags successfully created!'))   


    def create_questions(self, data, ratio):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        QuestionTag.objects.all().delete()

        tags = Tag.objects.all()
        users = User.objects.all()

        user_map = {user.username: user for user in users}
        tag_map = {tag.name: tag for tag in tags}

        questions = []
        answers = []
        questions_tags = []

        POOLS = 12  # количество потоков
        chunk_size = len(data) // POOLS
        data_chunks = [data[i * chunk_size: (i + 1) * chunk_size] for i in range(POOLS)]

        with ThreadPoolExecutor(max_workers=POOLS) as executor:
            futures = [executor.submit(self.process_chunk, chunk, user_map, tag_map) for chunk in data_chunks]

            for future in futures:
                future_result = future.result()
                if future_result:
                    chunk_questions, chunk_answers, chunk_questions_tags = future_result
                    questions.extend(chunk_questions)
                    answers.extend(chunk_answers)
                    questions_tags.extend(chunk_questions_tags)

        if len(questions) < ratio:
            self.command.stdout.write(self.command.style.ERROR('Not enough questions!'))
            return
        
        Question.objects.bulk_create(questions)
        Answer.objects.bulk_create(answers)
        QuestionTag.objects.bulk_create(questions_tags)

        self.command.stdout.write(self.command.style.SUCCESS(f'{len(questions)} questions successfully created!'))


    def process_chunk(self, data_chunk, user_map, tag_map):
        questions = []
        answers = []
        questions_tags = []

        for line in data_chunk:
            username = line['question_author_name']
            user = user_map.get(username)
            rating = int(line['question_rating'])

            question = Question(
                created_user=user,
                title=line['question_head'],
                rating=rating,
                text=line['question_text'],
                created_at=line['question_date'],
            )
            questions.append(question)

            tag_list = set()
            tag_list.add(line['question_category'])

            question_tag = QuestionTag(
                tag=tag_map[line['question_category']], 
                question=question,
            )
            questions_tags.append(question_tag)

            available_tags = set(tag_map.values()) - tag_list
            random_tags = random.sample(available_tags, k=min(4, len(available_tags)))
            for tag in random_tags:
                question_tag = QuestionTag(
                    tag=tag,
                    question=question,
                )
                questions_tags.append(question_tag)

            for ans_data in line['answers']:
                ans = line['answers'][ans_data]
                username = ans['answer_author_name']
                user = user_map.get(username)
                rating = int(ans['answer_rating'])

                answer = Answer(
                    created_user=user,
                    rating=rating,
                    text=ans['answer_text'],
                    question=question,
                )
                answers.append(answer)
        
        return questions, answers, questions_tags
    