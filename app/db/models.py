from django.db import models


class BaseAutoDate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseAutoDate):
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class TrainingSession(BaseAutoDate):
    corpus = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class WordHist(BaseAutoDate):
    word = models.CharField(max_length=255)
    corpus = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    training_session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
