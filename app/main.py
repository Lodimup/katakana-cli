import os
import random
import sys

import django
from corpus.kana import KATAKANA
from rich import print

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import TrainingSession, User, WordHist  # noqa: E402


def main():
    num_challenge = 20
    user_input = input("username: ")
    user, _ = User.objects.get_or_create(username=user_input)
    training_session = TrainingSession.objects.create(corpus="katakana", user=user)

    while num_challenge > 0:
        is_correct = False
        word = random.choice(list(KATAKANA.keys()))
        word_hist = WordHist.objects.create(
            word=word, corpus="katakana", training_session=training_session
        )
        correct_word = KATAKANA[word]
        user_input = input(f"{word}: ")

        if user_input == correct_word:
            is_correct = True

        if is_correct:
            sys.stdout.write("\033[F\033[K")
            word_hist.is_correct = is_correct
            print(f"{word}: {correct_word} [green]Correct![/green]")
        else:
            sys.stdout.write("\033[F\033[K")
            print(f"{word}: {correct_word} [red]Incorrect![/red]")

        word_hist.save()

        num_challenge -= 1

    print("Training session completed!")
    print("Review your answers:")
    correct_count = training_session.wordhist_set.filter(is_correct=True).count()
    incorrect_count = training_session.wordhist_set.filter(is_correct=False).count()
    for word_hist in training_session.wordhist_set.all():
        correct_word = KATAKANA.get(word_hist.word)
        hist_result_text = (
            "[green]Correct![/green]"
            if word_hist.is_correct
            else "[red]Incorrect![/red]"
        )
        print(f"{word_hist.word}: {correct_word} {hist_result_text}")
    print(f"[green]Correct[/green]: {correct_count}")
    print(f"[red]Incorrect[/red]: {incorrect_count}")


if __name__ == "__main__":
    main()
