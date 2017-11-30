# title          : load_questions.py
# description    : Read stored question data into python objects
# author         : Becker, Brett, Rawlinson
# date           : Tuesday, 28 November 2017.
# usage          : python load_questions.py
# ==================================================

import pickle
from random import randint
from quizlet_exams import subjects


def load_pkl_data(file_name):
    objects = []
    with (open(file_name, 'rb')) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects


def ask_questions(subject=None):
    for subject in subjects:
        input_file = 'question_data/' + subject + '_questions.pkl'
        subjects[subject] = load_pkl_data(input_file)

    response = ''
    questions = subjects['physics']

    while response != 'q':
        i = randint(0, len(questions) - 1)
        questions[i].print_question()
        print()
        response = input()
        print('\n', '-' * 50, '\n')

    return "A summary of your record so far"
