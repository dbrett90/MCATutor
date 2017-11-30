# title          : quizlet_exams.py
# description    : Scrape quizlet cards
# author         : Becker, Brett, Rawlinson
# date           : Friday,  3 November 2017.
# usage          : python3 quizlet_exams.py
# python_version : 3.6 (needed for pickle)
# ==================================================

import json
import requests
import pickle
import sys
import quizlet_regex as qr
from questionmc import QuestionMC

base_url = 'https://api.quizlet.com/2.0'
client_id = 'dWM9nE2PR2'
supersets = {
    "physics":    '248213509',
    "biology":    '248213153',
    "chemistry":  '248214260',
    "behavioral": '248214589'
}
subjects = {subject: [] for subject in supersets}


def parse_mc_terms(terms):
    questions = []
    for term in terms:
        choices = qr.get_choices_mc(term['term'])
        question = qr.get_question_mc(term['term'])
        answer = term['definition']
        if choices and question:
            questions.append(QuestionMC(question, choices, answer))

    return questions


def scrape_superset(subject):
    url = (base_url +
           '/sets/' + supersets[subject] +
           '?client_id=' + client_id)
    data = json.loads(requests.get(url).text)
    questions = parse_mc_terms(data['terms'])
    return questions


for subject in supersets:
    subjects[subject] = scrape_superset(subject)


for subject in subjects:
    txt_outfile = 'question_data/' + subject + '_questions.txt'
    sys.stdout = open(txt_outfile, 'w')
    for q in subjects[subject]:
        print(q)
        print('\n', '-' * 50, '\n')

    sys.stdout = sys.__stdout__

    json_qs = json.dumps([q.__dict__ for q in subjects[subject]])
    json_outfile = 'question_data/' + subject + '_questions.json'
    with open(json_outfile, 'w') as outfile:
        json.dump(json_qs, outfile)

    pkl_outfile = 'question_data/' + subject + '_questions.pkl'
    with open(pkl_outfile, 'wb') as outfile:
        for q in subjects[subject]:
            pickle.dump(q, outfile, pickle.HIGHEST_PROTOCOL)
