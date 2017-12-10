#!flask/bin/python

# import sys

from flask import Flask, render_template, request
import json
from ChatBot.chatbot import createChatbot
from ChatBot.load_questions import *

app = Flask(__name__)

bot = createChatbot()
ex_ready = False
exam = []
exam_length = 0
exam_ct = -1
exam_score = 0


@app.route('/')
def output():
    # serve index template
    return render_template('index.html', name='Joe')


@app.route('/receiver', methods=['POST'])
def worker():
    # read json + reply
    data = request.get_json()
    item = data[0]
    result = ''

    userResponse = str(item['input'])
    print("user response:")
    print(userResponse)

    result = bot.get_response(userResponse)

    question_request = result[:26] == "\nAbsolutely, here are some"
    subject = ''
    print(question_request)

    if question_request:
        subject = result.split()[4]

    json_obj = {'botResponse': result,
                'question_request': question_request,
                'index': -1,
                'subject': subject}

    return json.dumps(json_obj)


@app.route('/practice', methods=['POST'])
def administerQuestions():
    data = request.get_json()
    item = data[0]
    print(data)

    subject = ''
    state = 0
    subject = str(item['subject'])
    state = item['state']
    json_obj = {}
    botResponse = ''
    start_exam = False

    # quiz states:
    #     0: ask question
    #     1: check answer
    #     2: show correct answer
    #     3: give explanation
    if state == 0:
        botResponse, index = ask_question(subject)
        state = 1
    elif state == 1:
        userResponse = str(item['input'])
        index = item['index']
        if userResponse:
            userResponse = userResponse.lower()
            if userResponse in ['quit', 'q', 'stop']:
                botResponse = summary()
                index = -1
                subject = ''
                state = -1
            else:
                result = check_answer(subject, index, userResponse)
                if result:
                    next_question, index = ask_question(subject)
                    botResponse = "Correct!<br><br>" + next_question
                    state = 1
                else:
                    botResponse = (
                        "Sorry, it looks like that isn't correct.<br>" +
                        "Would you like to see the answer? y/n"
                    )
                    state = 2
        else:
            botResponse = "Sorry, I didn't get that."
            state = 1
    elif state == 2:
        userResponse = str(item['input'])
        index = item['index']
        userResponse = userResponse.lower()
        if userResponse in ['quit', 'q', 'stop']:
            botResponse = summary()
            index, subject, state = -1, '', -1
        elif userResponse in ['yes', 'y']:
            answer, has_explanation = get_answer(subject, index)
            botResponse = answer
            if has_explanation:
                botResponse += "<br><br>Would you like to see an explanation? y/n"
                state = 3
            else:
                q, index = ask_question(subject)
                botResponse += '<br><br><br>' + q
                state = 1
        else:
            botResponse, index = ask_question(subject)
            state = 1
    elif state == 3:
        userResponse = str(item['input'])
        index = item['index']
        userResponse = userResponse.lower()
        if userResponse in ['quit', 'q', 'stop']:
            botResponse = summary()
            index, subject, state = -1, '', -1
        elif userResponse in ['yes', 'y']:
            explanation = get_explanation(subject, index)
            question, index = ask_question(subject)
            botResponse = explanation + '<br><br><br>' + question
            state = 1
        else:
            botResponse, index = ask_question(subject)
            state = 1

    elif state == 4:
        userResponse = str(item['input'])
        if userResponse in ['yes', 'y']:
            # take the exam
            index, subject, state = -1, '', -1
            start_exam = True
    else:
        botResponse = "Something went wrong<br><br><br>" + summary()
        index, subject, state = -1, '', -1

    if state == -1 and exam_ready():
        botResponse += "<br><br>Would you like to take an exam?"
        index, subject, state = -1, '', 4

    json_obj = {'botResponse': botResponse,
                'index': index,
                'subject': subject,
                'state': state,
                'start_exam': start_exam}

    return json.dumps(json_obj)


def examSummary():
    msg = ("You got " + str(exam_score) + '/' +
           str(exam_ct + 1) +
           " correct on your exam!\n\n")
    return msg + summary()


@app.route('/exam', methods=['POST'])
def administerExam():
    data = request.get_json()
    item = data[0]
    print(data)

    botResponse = ''
    state = item['state']
    global exam_ct
    global exam
    global exam_score
    global exam_length

    if exam_ct == -1:
        print("REBUILDING EXAM")
        exam = build_exam()
        exam_length = len(exam)
        exam_ct += 1
        exam_score = 0

    finished = False

    if exam_ct >= exam_length:
        finished = True
        botResponse = examSummary()
        exam_ct, state = -1, -1
    elif state == 0:
        subject = exam[exam_ct][0]
        index = exam[exam_ct][1]
        question = subjects[subject][index]
        botResponse = question.getQuestion()
        state = 1
    elif state == 1:
        index = exam[exam_ct][1]
        userResponse = str(item['input'])
        if userResponse:
            index = exam[exam_ct][1]
            subject = exam[exam_ct][0]
            userResponse = userResponse.lower()
            if userResponse in ['quit', 'q', 'stop']:
                botResponse = examSummary()
                exam_ct, state = -1, -1
            else:
                result = check_answer(subject, index, userResponse)
                if result:
                    exam_score += 1
                    exam_ct += 1
                    if exam_ct >= exam_length:
                        finished = True
                        botResponse = examSummary()
                        exam_ct, state = -1, -1
                    else:
                        subject = exam[exam_ct][0]
                        index = exam[exam_ct][1]
                        next_question = subjects[subject][index].getQuestion()
                        botResponse = "Correct!<br><br>" + next_question
                        state = 1
                else:
                    botResponse = (
                        "Sorry, it looks like that isn't correct.<br>" +
                        "Would you like to see the answer?"
                    )
                    state = 2
        else:
            botResponse = "Sorry, I didn't get that."
            state = 1

    elif state == 2:
        index = exam[exam_ct][1]
        subject = exam[exam_ct][0]
        userResponse = str(item['input'])
        userResponse = userResponse.lower()
        if userResponse in ['quit', 'q', 'stop']:
            botResponse = examSummary()
            exam_ct, state = -1, -1
        elif userResponse in ['yes', 'y']:
            answer, has_explanation = get_answer(subject, index)
            botResponse = answer
            if has_explanation:
                botResponse += "<br><br>Would you like to see an explanation?"
                state = 3
            else:
                exam_ct += 1
                if exam_ct >= exam_length:
                    finished = True
                    botResponse = examSummary()
                    exam_ct, state = -1, -1
                else:
                    subject = exam[exam_ct][0]
                    index = exam[exam_ct][1]
                    q = subjects[subject][index].getQuestion()
                    botResponse += '<br><br><br>' + q
                    state = 1
        else:
            exam_ct += 1
            if exam_ct >= exam_length:
                finished = True
                botResponse = examSummary()
                exam_ct, state = -1, -1
            else:
                subject = exam[exam_ct][0]
                index = exam[exam_ct][1]
                botResponse = subjects[subject][index].getQuestion()
                state = 1

    elif state == 3:
        index = exam[exam_ct][1]
        subject = exam[exam_ct][0]
        userResponse = str(item['input'])
        userResponse = userResponse.lower()
        if userResponse in ['quit', 'q', 'stop']:
            botResponse = examSummary()
            exam_ct, state = -1, -1
        elif userResponse in ['yes', 'y']:
            explanation = get_explanation(subject, index)
            exam_ct += 1
            if exam_ct >= exam_length:
                finished = True
                botResponse = examSummary()
                exam_ct, state = -1, -1
            else:
                subject = exam[exam_ct][0]
                index = exam[exam_ct][1]
                question = subjects[subject][index].getQuestion()
                botResponse = explanation + '<br><br><br>' + question
                state = 1
        else:
            exam_ct += 1
            if exam_ct >= exam_length:
                finished = True
                botResponse = examSummary()
                exam_ct, state = -1, -1
            else:
                subject = exam[exam_ct][0]
                index = exam[exam_ct][1]
                botResponse = subjects[subject][index].getQuestion()
                state = 1
    else:
        botResponse = "Something went wrong<br><br><br>" + examSummary()
        exam_ct, subject, state = -1, '', -1

    botResponse = botResponse.replace('\n', '<br>')

    json_obj = {'botResponse': botResponse,
                'state': state,
                'finished': finished}

    return json.dumps(json_obj)


if __name__ == '__main__':
    app.debug = True
    # run!
    app.run()
