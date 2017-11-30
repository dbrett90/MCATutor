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
import sys
import quizlet_regex as qr
from questionmc import QuestionMC
from questionid import QuestionID


base_url = 'https://api.quizlet.com/2.0'
client_id = 'dWM9nE2PR2'
class_id_mc = '5810856'
url_mc = (base_url +
          '/classes/' + class_id_mc +
          '/sets' +
          '?client_id=' + client_id)
data_mc = json.loads(requests.get(url_mc).text)

class_id_mc_rev = '5812982'
url_mc_rev = (base_url +
              '/classes/' + class_id_mc_rev +
              '/sets' +
              '?client_id=' + client_id)
data_mc_rev = json.loads(requests.get(url_mc_rev).text)

class_id_id = '5824458'
url_id = (base_url +
          '/classes/' + class_id_id +
          '/sets' +
          '?client_id=' + client_id)
data_id = json.loads(requests.get(url_id).text)


def parse_mc_terms(terms):
    questions = []
    for term in terms:
        choices = qr.get_choices_mc(term['term'])
        question = qr.get_question_mc(term['term'])
        answer = term['definition']
        if choices and question:
            questions.append(QuestionMC(question, choices, answer))

    return questions


def parse_mc_terms_rev(terms):
    questions = []
    for term in terms:
        choices = qr.get_choices_mc(term['definition'])
        question = qr.get_question_mc(term['definition'])
        answer = term['term'].strip()
        if choices and question and answer:
            questions.append(QuestionMC(question, choices, answer))

    return questions


def parse_id_terms(terms):
    questions = []
    for term in terms:
        question, answer = qr.get_question_id(term)
        if question and answer:
            questions.append(QuestionID(question, answer))

    return questions


mc_questions = []
id_questions = []

for card_set in data_mc:
    for q in parse_mc_terms(card_set['terms']):
        mc_questions.append(q)

for card_set in data_mc_rev:
    for q in parse_mc_terms_rev(card_set['terms']):
        mc_questions.append(q)

for card_set in data_id:
    for q in parse_id_terms(card_set['terms']):
        id_questions.append(q)


print("Multiple choice questions found:", len(mc_questions))
print("Defninition/SA questions found: ", len(id_questions))

sys.stdout = open('question_data/mc_questions.txt', 'w')
for q in mc_questions:
    print(q)
    print('\n', '-' * 50, '\n')

sys.stdout = open('question_data/id_questions.txt', 'w')
for q in id_questions:
    print(q)
    print('\n', '-' * 50, '\n')


mc_json = json.dumps([q.__dict__ for q in mc_questions])
with open('question_data/mc_questions.json', 'w') as outfile:
    json.dump(mc_json, outfile)

with open('question_data/mc_questions.pkl', 'wb') as output:
    for q in mc_questions:
        pickle.dump(q, output, pickle.HIGHEST_PROTOCOL)

id_json = json.dumps([q.__dict__ for q in mc_questions])
with open('question_data/id_questions.json', 'w') as outfile:
    json.dump(id_json, outfile)

with open('question_data/id_questions.pkl', 'wb') as output:
    for q in id_questions:
        pickle.dump(q, output, pickle.HIGHEST_PROTOCOL)
