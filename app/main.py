import os
import random
import sys

import django
from corpus.kana import KATAKANA
from rich import print
from rich.progress import Progress
from rich.table import Table

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from db.models import TrainingSession, User, WordHist  # noqa: E402

CORPUS_NAME = "katakana"
CORPUS = KATAKANA


def main():
    num_challenge = 20
    selected_incorrect_words = []
    user_input = input("username: ")
    user, _ = User.objects.get_or_create(username=user_input)
    prev_training_session = (
        TrainingSession.objects.filter(user=user).order_by("-created").first()
    )
    words = random.sample(list(CORPUS.keys()), num_challenge)
    if prev_training_session:
        incorrect_words = prev_training_session.wordhist_set.filter(
            is_correct=False
        ).values_list("word", flat=True)
        selected_incorrect_words = random.sample(
            list(incorrect_words), min(5, len(incorrect_words))
        )
        words += selected_incorrect_words
        random.shuffle(words)

    # start training session
    training_session = TrainingSession.objects.create(corpus=CORPUS_NAME, user=user)
    print(f"previous incorrect words: {', '.join(selected_incorrect_words)}")

    with Progress() as progress:
        task = progress.add_task("Training...", total=len(words))
        for word in words:
            is_correct = False
            word_hist = WordHist.objects.create(
                word=word, corpus=CORPUS_NAME, training_session=training_session
            )
            correct_word = CORPUS[word]
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
                while True:
                    user_input = input(f"{word}: ")
                    if user_input == correct_word:
                        print(f"{word}: {correct_word} [green]OK![/green]")
                        break

            word_hist.save()
            progress.advance(task)

    print("Training session completed!")
    print("Review your answers:")

    table = Table(title="Training Summary")
    table.add_column("Word", justify="center")
    table.add_column("Correct Word", justify="center")
    table.add_column("Result", justify="center")

    correct_count = training_session.wordhist_set.filter(is_correct=True).count()
    incorrect_count = training_session.wordhist_set.filter(is_correct=False).count()
    for word_hist in training_session.wordhist_set.all():
        correct_word = CORPUS.get(word_hist.word)
        hist_result_text = (
            "[green]Correct![/green]"
            if word_hist.is_correct
            else "[red]Incorrect![/red]"
        )
        table.add_row(word_hist.word, correct_word, hist_result_text)

    print(table)
    print(f"[green]Correct[/green]: {correct_count}")
    print(f"[red]Incorrect[/red]: {incorrect_count}")


if __name__ == "__main__":
    main()
