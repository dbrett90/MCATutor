# title          : load_questions.py
# description    : Read stored question data into python objects
# author         : Becker, Brett, Rawlinson
# date           : Tuesday, 28 November 2017.
# usage          : python load_questions.py
# ==================================================

import pickle
from random import randint, sample
from util import listify

exam_length = 5

# scoring = {
#     "physics":    [3.0, 1.0],
#     "biology":    [3.0, 2.0],
#     "chemistry":  [3.0, 1.0],
#     "behavioral": [4.0, 3.0]
# }
scoring = {
    "physics":    [0.0, 0.0],
    "biology":    [0.0, 0.0],
    "chemistry":  [0.0, 0.0],
    "behavioral": [0.0, 0.0]
}
subjects = {subject: [] for subject in scoring}


def load_pkl_data(file_name):
    objects = []
    with (open(file_name, 'rb')) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    return objects


for s in subjects:
    input_file = '../Data/question_data/' + s + '_questions.pkl'
    subjects[s] = load_pkl_data(input_file)


def summary():
    msg = "Here's a summary your record so far:<br>"
    for s in scoring:
        if scoring[s][0] > 0.0:
            pctg = "{0:.0f}%".format(scoring[s][1] / scoring[s][0] * 100)
            msg += s + ': ' + pctg + '<br>'

    return msg


def ask_question(subject):
    response = ''
    questions = subjects[subject]

    i = randint(0, len(questions) - 1)
    q = questions[i]
    response += "Difficulty: " + str(q.difficulty) + "\n"
    response += q.getQuestion()

    return response.replace('\n', '<br>'), i


def check_answer(subject, index, guess):
    questions = subjects[subject]

    correct = questions[index].check_answer(guess)
    scoring[subject][0] += 1.0
    if correct:
        questions[index].update_difficulty(1)
        scoring[subject][1] += 1.0
        print("Correct!")
        return True

    return False


def get_answer(subject, index):
    q = subjects[subject][index]
    ans = q.answer.replace('\n', '<br>')
    has_explanation = q.explanation != ''
    return ans, has_explanation


def get_explanation(subject, index):
    return subjects[subject][index].explanation.replace('\n', '<br>')


def exam_ready():
    return all([scoring[s][1] >= 1.0 for s in scoring])


def heuristic(subject, num):
    questions = sample(range(len(subjects[subject])), num)

    return questions


def build_exam():
    inv_pcts = {s: 1.0 / scoring[s][1] / scoring[s][0] for s in subjects}
    rel_pcts = {s: inv_pcts[s] / sum(inv_pcts.values()) for s in subjects}
    num_qs = {s: int(round(exam_length * rel_pcts[s])) for s in rel_pcts}
    exam = {s: heuristic(s, num_qs[s]) for s in scoring}

    return listify(exam)
