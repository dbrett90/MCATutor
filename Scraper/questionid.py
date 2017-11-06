from pprint import pformat


class QuestionID:

    """A question, choices, and answer."""

    def __init__(self, question, answer):
        self._question = question
        self._answer = answer

    def question(self):
        return self._question

    def answer(self):
        return self._answer

    def __str__(self):
        str = ('Q: ' + self.question() + '\n' +
               'A: ' + self.answer())
        return str
