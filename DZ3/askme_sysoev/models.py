from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta

class QuestionManager(models.Manager):
    def best(self):
        return self.order_by('-rating')

    def newest(self):
        return self.order_by('-created_at')
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/', null=True, blank=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    mark = models.BooleanField()


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = QuestionManager()


class QuestionLike(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('like', 'question')


class Answer(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswerLike(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)  # Corrected to reference Answer

    class Meta:
        unique_together = ('like', 'answer')


class Tag(models.Model):
    name = models.CharField(max_length=255)


class QuestionTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
