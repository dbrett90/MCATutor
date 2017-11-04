from pprint import pformat


class Question:

    """A question, choices, and answer."""

    def __init__(self, question, choices, answer):
        self._question = question
        self._choices = choices
        self._answer = answer

    def question(self):
        return self._question

    def choices(self):
        return self._choices

    def answer(self):
        return self._answer

    def __str__(self):
        str = (self.question() + '\n' +
               pformat(self.choices()) + '\n' +
               self.answer())
        return str
