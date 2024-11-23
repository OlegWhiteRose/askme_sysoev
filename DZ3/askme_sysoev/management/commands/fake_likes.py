import random
from django.contrib.auth.models import User
from askme_sysoev.models import Question, Answer, QuestionLike, AnswerLike
from django.db import transaction

def fill_likes(ratio):
    QuestionLike.objects.all().delete()
    AnswerLike.objects.all().delete()

    users = User.objects.all()
    questions = Question.objects.all()
    answers = Answer.objects.all()

    if not users.exists() or not questions.exists() or not answers.exists():
        print("Not enough data for likes")
        return

    user_list = list(users)
    question_list = list(questions)
    answer_list = list(answers)

    questions_likes = []
    answers_likes = []

    def gen_unique(q, param1, param2):
        key = random.choice(param1)
        value = random.choice(param2)
        if key not in q:
            q[key] = set()

        while value in q[key]:
            key = random.choice(param1)
            value = random.choice(param2)

        q[key].add(value)

        return key, value

    with transaction.atomic():
        q = {}
        for _ in range(ratio):
            user, question = gen_unique(q, user_list, question_list)
            question_like = QuestionLike(
                mark=True,
                user=user, 
                question=question 
            )
            questions_likes.append(question_like)
            
            user, answer = gen_unique(q, user_list, answer_list)
            answer_like = AnswerLike(
                mark=True,
                user=user, 
                answer=answer
            )
            answers_likes.append(answer_like)

        QuestionLike.objects.bulk_create(questions_likes)
        AnswerLike.objects.bulk_create(answers_likes)

    print(f"Created {len(questions_likes) + len(answers_likes)} likes!")
