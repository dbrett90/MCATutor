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
import re
from orderedset import OrderedSet
from pprint import pprint

base_url = 'https://api.quizlet.com/2.0'
client_id = 'dWM9nE2PR2'
class_id = '5810856'
url = (base_url +
       '/classes/' + class_id +
       '/sets' +
       '?client_id=' + client_id)

choice_patterns = ["\n[Aa].*\n[Bb]",
                   "\n[Bb].*\n[Cc]",
                   "\n[Cc].*\n[Dd]",
                   "\n[Dd].*\n[Ee]",
                   "\n[De].*",
                   "\n[Ee].*"]

strip_patterns = ["[ABCDEabcde]\..*", "[ABCDEabcde].*"]


def get_options(question):
    choices_raw = []
    choices = OrderedSet()
    for pattern in choice_patterns:
        matchObject = re.search(pattern, question, flags=0)
        if matchObject:
            match = matchObject.group(0)
            if match[-2] == '\n':
                choices_raw.append(match[1:-2])
            else:
                choices_raw.append(match[1:])

    for i in range(len(choices_raw)):
        matchObject = re.search(strip_patterns[0],
                                choices_raw[i],
                                flags=0)
        if matchObject:
            choices.add(matchObject.group(0)[3:])
        else:
            matchObject = re.search(strip_patterns[1],
                                    choices_raw[i],
                                    flags=0)
            if matchObject:
                choices.add(matchObject.group(0)[2:])

    return list(choices)


response = requests.get(url)

data = json.loads(response.text)


questions = []
for term in data[1]['terms']:
    choices = get_options(term['term'])
    if choices:
        questions.append(choices)


for term in data[2]['terms']:
    choices = get_options(term['term'])
    if choices:
        questions.append(choices)


pprint(questions)
print(len(questions))
