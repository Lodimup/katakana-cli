import os
import random
import sys

import django
from corpus.kana import KATAKANA
from rich import print

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import WordStat  # noqa: E402


def main():
    while True:
        word = random.choice(list(KATAKANA.keys()))
        correct_word = KATAKANA[word]
        user_input = input(f"{word}: ")

        word_stat = WordStat.objects.filter(word=word, corpus="katakana").first()
        if word_stat is None:
            word_stat = WordStat(word=word, corpus="katakana")

        if user_input == correct_word:
            word_stat.correct += 1
            sys.stdout.write("\033[F\033[K")
            print(f"{word}: {correct_word} [green]Correct![/green]")
        else:
            word_stat.incorrect += 1
            sys.stdout.write("\033[F\033[K")
            print(f"{word}: {correct_word} [red]Incorrect![/red]")
        word_stat.save()


if __name__ == "__main__":
    main()
