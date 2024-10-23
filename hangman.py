import json
from wonderwords import RandomWord
import pyfiglet
import random
import os

with open('data.json', 'r') as file:
    parsed_answers = json.load(file)


sudden_win = parsed_answers["answers"]["victory"]["suddenWin"]
guessed_word = parsed_answers["answers"]["victory"]["guessedWord"]
lost_tries = parsed_answers["answers"]["fail"]["lostTries"]

correct_guesses = parsed_answers["answers"]["guesses"]["correctGuess"]
wrong_guesses = parsed_answers["answers"]["guesses"]["wrongGuess"]
same_guesses = parsed_answers["answers"]["guesses"]["sameGuess"]


class Hangman:
    def __init__(self, word):
        self._word = word
        self.guessed = [" _ " for _ in range(len(word))]
        self.letters = []
        self.mistakes = 6

    def format_text(self, argument):
        return """
{argument}
Guessed letters: {letters}

Word: {word}
Tries left: {tries}
""".format(
            argument=argument,
            letters=self.letters,
            word=" ".join(self.guessed),
            tries=self.mistakes
        )

    def end_game(self, message):
        return """
{message}

The word was '{word}'.
Thanks for playing!
        """.format(message=message, word=self._word)

    def check_involvement(self, letter):

        if letter in self._word:

            for guessed_index in range(len(self._word)):
                if self._word[guessed_index] == letter:
                    self.change_guessed_letters(guessed_index, letter)

            if letter not in self.letters:
                self.letters.append(letter)

            return self.format_text(
                argument=random.choice(correct_guesses)
            )

        else:
            if letter in self.letters:

                return self.format_text(
                    argument=random.choice(same_guesses)
                )
            else:

                self.mistakes -= 1
                self.letters.append(letter)

                return self.format_text(
                    argument=random.choice(wrong_guesses)
                )

    def change_guessed_letters(self, index, letter):
        self.guessed[index] = letter

    def check_word_equality(self):
        return "".join(self.guessed) == self._word

    def check_word_fully(self, entered_word):
        return entered_word == self._word


def start_game():

    # Initialize custom font object
    f = pyfiglet.figlet_format("Hangman", font="ansi_shadow")
    print(f)

    # Creates a random word from 'wonderwords' library
    r = RandomWord().word()
    hangman_instance = Hangman(r)

    text = f"""
Welcome to the hell of Hangman )-)
I hope you know the rules, and if you don't, well, too bad he-he :)

The word has already been generated, so good luck <3

{" ".join([" _ " for _ in r])}
"""

    print(text)

    while hangman_instance.mistakes > 0:
        letter = str(input("Please enter a letter: "))
        if letter.isalpha() and len(letter) == 1:
            result = hangman_instance.check_involvement(letter)
            print(result)
            if hangman_instance.check_word_equality():
                print(hangman_instance.end_game(random.choice(guessed_word)))
                break
        else:
            if hangman_instance.check_word_fully(letter):
                print(hangman_instance.end_game(random.choice(sudden_win)))
                break

    if hangman_instance.mistakes == 0:
        print(hangman_instance.end_game(random.choice(lost_tries)))

    again = str(input("Would you like to play on more time? y/n: "))
    if again == "y":

        # Clears a terminal
        os.system('cls || clear')
        return start_game()
    else:

        # Initialize custom font object
        f = pyfiglet.figlet_format("END GAME", font="ansi_shadow")
        print(f)
        return True


if __name__ == '__main__':
    start_game()
