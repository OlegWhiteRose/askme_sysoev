import random
from django.contrib.auth.models import User
from askme_sysoev.models import Question, Answer, Like, QuestionLike, AnswerLike
from django.db import transaction

def fill_likes(ratio):
    Like.objects.all().delete()
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

    likes = []
    questions_likes = []
    answers_likes = []

    with transaction.atomic():
        for _ in range(ratio):
            like = Like(
                mark=True,
                user=random.choice(user_list) 
            )
            likes.append(like)

            if random.choice([True, False]):
                question_like = QuestionLike(
                    like=like,
                    question=random.choice(question_list) 
                )
                questions_likes.append(question_like)
            else:
                answer_like = AnswerLike(
                    like=like,
                    answer=random.choice(answer_list) 
                )
                answers_likes.append(answer_like)

        Like.objects.bulk_create(likes)
        QuestionLike.objects.bulk_create(questions_likes)
        AnswerLike.objects.bulk_create(answers_likes)

    print(f"Created {len(likes)} likes!")
