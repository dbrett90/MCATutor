#!flask/bin/python

# import sys

from flask import Flask, render_template, request, redirect, Response
import json
from ChatBot.chatbot import createChatbot
from ChatBot.load_questions import subjects, ask_question

app = Flask(__name__)

bot = createChatbot()


@app.route('/output')
def output():
    # serve index template
    return render_template('index.html', name='Joe')


@app.route('/receiver', methods=['POST'])
def worker():
    # read json + reply
    data = request.get_json()
    result = ''

    for item in data:
        # loop over every row
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

    subject = ''
    for item in data:
        print(item)
        subject = str(item['subject'])

    question = ask_question(subject).replace('\n', '<br>')

    return json.dumps({'botResponse': question})


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

# The following loop will execute each time the user enters input
# while True:
#     try:
#         # We pass None to this method because the parameter
#         # is not used by the TerminalAdapter
#         txt = input()
#         bot_input = bot.get_response(txt)
#         # bot_input = bot.get_response(None)

#         if bot_input[:26] == "\nAbsolutely, here are some":
#             print("(Enter 'q' to quit and select a new topic.)\n")
#             subject = bot_input.split()[4]
#             ask_questions(subject)

#     # Press ctrl-c or ctrl-d on the keyboard to exit
#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break


if __name__ == '__main__':
    app.debug = True
    # run!
    app.run()
