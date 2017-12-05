from pprint import pformat
from string import ascii_uppercase


class QuestionMC:

    """A question, choices, and answer."""

    def __init__(self, question, choices, answer, explanation=''):
        self._question = question
        self._choices = choices
        self._answer = answer
        self._explanation = explanation

    def question(self):
        return self._question

    def choices(self):
        return self._choices

    def answer(self):
        return self._answer

    def explanation(self):
        return self._explanation

    def check_answer(self, guess):
        guess = guess[0].lower()
        answer = self.answer()[0].lower()
        return guess == answer

    def print_question(self):
        print(self.question(), '\n')

        for i in range(len(self._choices)):
            print(ascii_uppercase[i] + '. ' + self._choices[i])

    def __str__(self):
        str = (self.question() + '\n' +
               pformat(self.choices()) + '\n' +
               self.answer())

        expl = self.explanation()
        if expl:
            str += '\n' + 'Explanation:\n' + expl
        return str
