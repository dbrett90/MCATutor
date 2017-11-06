# title           : readexam.py
# description     :
# author          : Becker, Brett, Rawlinson
# date            : Friday, 27 October 2017.
# version         :
# usage           : python readexam.py path/to/file.json
# notes           :
# python_version  : python 2.7.13
# ==================================================

import sys
import json
from pprint import pprint
from questionmc import QuestionMC
from section import Section


def parse_section(section):
    questions = []

    passage = section['passage']
    json_questions = section['questions']

    for json_question in json_questions:
        question = json_question['question']
        choices = json_question['choices']
        answer = json_question['answer']

        questions.append(QuestionMC(question, choices, answer))

    return Section(passage, questions)


def main():
    json_file = open(sys.argv[1])
    json_str = json_file.read()
    json_data = json.loads(json_str)
    json_exam = json_data['sections']
    exam = []

    for section in json_exam:
        exam.append(parse_section(section))

    pprint(exam[1].questions()[0].choices())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Read exam data from a JSON file\n" +
              "Usage: python " +
              sys.argv[0] +
              " path/to/file.json")
    else:
        main()
