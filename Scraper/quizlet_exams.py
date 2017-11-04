# title          : quizlet_exams.py
# description    :
# author         : Becker, Brett, Rawlinson
# date           : Friday,  3 November 2017.
# version        :
# usage          :
# notes          :
# python_version :
# ==================================================

import json
import requests
import pickle
import quizlet_regex as qr
from question import Question


base_url = 'https://api.quizlet.com/2.0'
client_id = 'dWM9nE2PR2'
class_id = '5810856'
url = (base_url +
       '/classes/' + class_id +
       '/sets' +
       '?client_id=' + client_id)
response = requests.get(url)
data = json.loads(response.text)

class_id_rev = '5812982'
url_rev = (base_url +
           '/classes/' + class_id_rev +
           '/sets' +
           '?client_id=' + client_id)
data_rev = json.loads(requests.get(url_rev).text)


def parse_terms(terms):
    questions = []
    for term in terms:
        choices = qr.get_options(term['term'])
        question = qr.get_question(term['term'])
        answer = term['definition']
        if choices and question:
            questions.append(Question(question, choices, answer))

    return questions


def parse_terms_rev(terms):
    questions = []
    for term in terms:
        choices = qr.get_options(term['definition'])
        question = qr.get_question(term['definition'])
        answer = term['term']
        if choices and question:
            questions.append(Question(question, choices, answer))

    return questions


test_questions = []
for card_set in data:
    for q in parse_terms(card_set['terms']):
        test_questions.append(q)
        # print(q)
        # print('\n', '-' * 50, '\n')

for card_set in data_rev:
    for q in parse_terms_rev(card_set['terms']):
        test_questions.append(q)
        # print(q)
        # print('\n', '-' * 50, '\n')


print("Questions found:", len(test_questions))

s = json.dumps([q.__dict__ for q in test_questions])
with open('quizlet_data.txt', 'w') as outfile:
    json.dump(s, outfile)

with open('quizlet_data.pkl', 'wb') as output:
    for q in test_questions:
        pickle.dump(q, output, pickle.HIGHEST_PROTOCOL)
