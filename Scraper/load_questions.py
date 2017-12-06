# title          : load_questions.py
# description    : Read stored question data into python objects
# author         : Becker, Brett, Rawlinson
# date           : Tuesday, 28 November 2017.
# usage          : python load_questions.py
# ==================================================

import pickle
from random import randint

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


def summary():
    print("\nHere's a summary your record so far:")
    for s in scoring:
        if scoring[s][0] > 0.0:
            pctg = "{0:.0f}%".format(scoring[s][1] / scoring[s][0] * 100)
            msg = s + ': ' + pctg
            print(msg)


def ask_questions(subject):
    for s in subjects:
        input_file = '../Data/question_data/' + s + '_questions.pkl'
        subjects[s] = load_pkl_data(input_file)

    response = ''
    questions = subjects[subject]

    while response != 'q':
        i = randint(0, len(questions) - 1)
        print("Difficulty:", questions[i].difficulty)
        questions[i].print_question()
        print()
        response = input()
        if response == 'q':
            break

        correct = questions[i].check_answer(response)
        scoring[subject][0] += 1.0
        if correct:
            questions[i].update_difficulty(1)
            scoring[subject][1] += 1.0
            print("Correct!")
        else:
            questions[i].update_difficulty(0)
            print("\nSorry, it looks like that isn't correct.\n" +
                  "Would you like to see the answer? y/n\n")
            response = input()
            response = response.lower()
            if response == "yes" or response == 'y':
                print('\n' + questions[i].answer)

            explanation = questions[i].explanation
            if explanation:
                print("\nWould you like to see an explanation? y/n\n")
                response = input()
                response = response.lower()
                if response == "yes" or response == 'y':
                    print('\n' + explanation)

        print('\n', '-' * 50, '\n')

    summary()

    print("\nWhat subject would you like to study?\n" +
          "(press ctrl-d or ctrl-c to quit)\n")


def build_exam():
    return None
