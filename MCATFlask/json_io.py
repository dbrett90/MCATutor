#!flask/bin/python

# import sys

from flask import Flask, render_template, request, redirect, Response
import json
from ChatBot.chatbot import createChatbot
from ChatBot.load_questions import subjects, ask_question, check_answer,\
    get_answer, get_explanation, summary

app = Flask(__name__)

bot = createChatbot()


@app.route('/')
def output():
    # serve index template
    # return redirect("http://www.mcatutor.com", code=302)
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

    # print("(Enter 'q' to quit and select a new topic.)\n")
    # ask_questions(subject)

    json_obj = {'botResponse': result,
                'question_request': question_request,
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

    # quiz states:
    #     0: ask question
    #     1: check answer
    #     2: show correct answer
    #     3: give explanation
    if state == 0:
        question, index = ask_question(subject)
        # question = question.replace('\n', '<br>')
        json_obj = {'botResponse': question,
                    'index': index,
                    'subject': subject,
                    'state': 1}
    elif state == 1:
        print("in state 1")
        userResponse = str(item['input'])
        index = item['index']
        if userResponse:
            userResponse = userResponse.lower()
            if userResponse in ['quit', 'q', 'stop']:
                json_obj = {'botResponse': summary(),
                            'index': -1,
                            'subject': '',
                            'state': -1}
            else:
                botResponse = ''
                result = check_answer(subject, index, userResponse)
                if result:
                    next_question, index = ask_question(subject)
                    botResponse = "Correct!<br><br>" + next_question
                    json_obj = {'botResponse': botResponse,
                                'index': index,
                                'subject': subject,
                                'state': 1}
                else:
                    botResponse = (
                        "Sorry, it looks like that isn't correct.\n" +
                        "Would you like to see the answer? y/n"
                    )
                    json_obj = {'botResponse': botResponse,
                                'index': index,
                                'subject': subject,
                                'state': 2}
        else:
            botResponse = "Sorry, I didn't get that."
            json_obj = {'botResponse': botResponse,
                        'index': index,
                        'subject': subject,
                        'state': 1}
    elif state == 2:
        userResponse = str(item['input'])
        index = item['index']
        # if userResponse:
        userResponse = userResponse.lower()
        if userResponse in ['quit', 'q', 'stop']:
            json_obj = {'botResponse': summary(),
                        'index': -1,
                        'subject': '',
                        'state': -1}
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

            json_obj = {'botResponse': botResponse,
                        'index': index,
                        'subject': subject,
                        'state': state}
        else:
            botResponse, index = ask_question(subject)
            json_obj = {'botResponse': botResponse,
                        'index': index,
                        'subject': subject,
                        'state': 1}
    elif state == 3:
        userResponse = str(item['input'])
        index = item['index']
        # if userResponse:
        userResponse = userResponse.lower()
        if userResponse in ['quit', 'q', 'stop']:
            json_obj = {'botResponse': summary(),
                        'index': -1,
                        'subject': '',
                        'state': -1}
        elif userResponse in ['yes', 'y']:
            explanation = get_explanation(subject, index)
            question, index = ask_question(subject)
            botResponse = explanation + '<br><br><br>' + question
            json_obj = {'botResponse': botResponse,
                        'index': index,
                        'subject': subject,
                        'state': 1}
        else:
            question, index = ask_question(subject)
            json_obj = {'botResponse': question,
                        'index': index,
                        'subject': subject,
                        'state': 1}
    else:
        json_obj = {'botResponse': "Something went wrong",
                    'index': -1,
                    'subject': '',
                    'state': -1}

    return json.dumps(json_obj)


welcome_msg = ("""
Welcome to MCATutor!

I am an AI chatbot that would like to help you study for your MCAT
exam. I have a collection of questions from subjects including:
""" +
               '- ' +
               '\n- '.join(s for s in subjects) +
               " science" +
               '\n' * 2 +
               'What would you like to study today?\n')

if __name__ == '__main__':
    app.debug = True
    # run!
    app.run()
