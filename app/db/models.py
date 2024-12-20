from django.db import models


class WordStat(models.Model):
    word = models.CharField(max_length=255)
    corpus = models.CharField(max_length=255)
    correct = models.PositiveIntegerField(default=0)
    incorrect = models.PositiveIntegerField(default=0)
