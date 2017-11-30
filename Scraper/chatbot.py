# title          : chatbot.py
# description    : Chat interface for MCATutor
# author         : Becker, Brett, Rawlinson
# date           : Wednesday, 29 November 2017.
# usage          : python3 chatbot.py
# python_version : 3.6
# ==================================================

import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from load_questions import ask_questions, subjects

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

db_exists = os.path.exists("database.db")

# Create a new instance of a ChatBot
bot = ChatBot(
    "MCATutor",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        "chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    database="database"
)


def train_subject_prompts():
    for s in subjects:
        bot_res = "\nAbsolutely, here are some " + s + " questions:\n"
        phrases = [
            s,
            "Please quiz me on " + s,
            "Ask me questions about " + s,
            "Can you quiz me on " + s,
            "Can you give me " + s + " questions?",
            "How about some " + s + " questions?",
            "I would like to practice " + s + " questions"
        ]

        for phrase in phrases:
            bot.train([phrase, bot_res])


if not db_exists:
    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train("chatterbot.corpus.english")
    bot.train("chatterbot.corpus.english.greetings")

    bot.set_trainer(ListTrainer)
    train_subject_prompts()


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


print(welcome_msg)


# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

        if bot_input[:26] == "\nAbsolutely, here are some":
            print("(Enter 'q' to quit and select a new topic.)\n")
            subject = bot_input.split()[4]
            ask_questions(subject)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
