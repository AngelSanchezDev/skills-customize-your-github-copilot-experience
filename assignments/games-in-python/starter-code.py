"""Starter code for Hangman game assignment.

This scaffold provides helper functions and a `main()` you can complete
or extend for bonus features. Run with `python3 starter-code.py`.
"""

import random
from typing import List


WORD_LIST: List[str] = [
	"python",
	"hangman",
	"challenge",
	"programming",
	"computer",
]


def choose_word(words: List[str]) -> str:
	"""Return a random word from the provided list."""
	return random.choice(words)


def display_progress(secret: str, guessed: set) -> str:
	"""Return a string showing guessed letters and underscores for hidden ones."""
	return " ".join([c if c in guessed else "_" for c in secret])


def main():
	secret_word = choose_word(WORD_LIST)
	guessed_letters = set()
	incorrect_guesses = 0
	max_incorrect = 6

	print("Welcome to Hangman! Guess letters to reveal the secret word.")

	while incorrect_guesses < max_incorrect and any(c not in guessed_letters for c in secret_word):
		print("\nWord:", display_progress(secret_word, guessed_letters))
		print(f"Incorrect guesses: {incorrect_guesses}/{max_incorrect}")
		guess = input("Enter a single letter: ").strip().lower()
		if not guess or len(guess) != 1 or not guess.isalpha():
			print("Please enter a single alphabetical character.")
			continue
		if guess in guessed_letters:
			print("You already guessed that letter.")
			continue
		guessed_letters.add(guess)
		if guess not in secret_word:
			incorrect_guesses += 1

	if all(c in guessed_letters for c in secret_word):
		print(f"\nCongratulations — you guessed the word: {secret_word}")
	else:
		print(f"\nGame over. The secret word was: {secret_word}")


if __name__ == "__main__":
	main()
