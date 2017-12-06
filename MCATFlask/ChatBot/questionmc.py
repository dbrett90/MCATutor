from pprint import pformat
from string import ascii_uppercase
import nltk


class QuestionMC:

    """A question, choices, and answer."""

    def __init__(self, question, choices, answer, explanation=''):
        self._question = question
        self._choices = choices
        self._answer = answer
        self._explanation = explanation
        self._initial_difficulty = 0
        self._difficulty = {'total': 0, 'correct': 0}

    @property
    def question(self):
        return self._question

    @property
    def choices(self):
        return self._choices

    @property
    def answer(self):
        return self._answer

    @property
    def explanation(self):
        return self._explanation

    @property
    def difficulty(self):
        if self._difficulty['total']:
            diff = (float(self._difficulty['correct']) /
                    float(self._difficulty['total']))
            return diff

        return self._initial_difficulty

    def update_difficulty(self, correct):
        self._difficulty['total'] += 1
        if correct:
            self._difficulty['correct'] += 1

    def check_answer(self, guess):
        guess = guess[0].lower()
        answer = self.answer[0].lower()
        return guess == answer

    @staticmethod
    def txt_complexity(text):
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)

        return len(entities)

    def set_initial_difficulty(self):
        question_complexity = self.txt_complexity(self.question)
        choice_complexity = [self.txt_complexity(c) for c in self.choices]
        choice_complexity = sum(choice_complexity) // len(choice_complexity)

        compl = (question_complexity + choice_complexity)
        self._initial_difficulty = compl // 10

    def print_question(self):
        print(self.question, '\n')

        for i in range(len(self.choices)):
            print(ascii_uppercase[i] + '. ' + self._choices[i])

    def getQuestion(self):
        question = self.question + '\n'

        for i in range(len(self.choices)):
            question += ascii_uppercase[i] + '. ' + self._choices[i] + '\n'

        return question

    def __str__(self):
        output = ("Level: " + str(self.difficulty) + '\n' +
                  self.question + '\n' +
                  pformat(self.choices) + '\n' +
                  self.answer)

        expl = self.explanation
        if expl:
            output += '\n' + 'Explanation:\n' + expl
        return output
