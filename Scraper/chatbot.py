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
from load_questions import ask_questions

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

if not db_exists:
    bot.set_trainer(ChatterBotCorpusTrainer)
    bot.train("chatterbot.corpus.english")
    bot.train("chatterbot.corpus.english.greetings")

bot.set_trainer(ListTrainer)


bot.train(["I'd like some MCAT Questions Please",
           "Absolutely, from what section of the exam?",
           "Please quiz me on some Multiple Choice Questions",
           "Absolutely, here are some questions:\n"])

print("Type something to begin...")


# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        bot_input = bot.get_response(None)

        if bot_input == "Absolutely, here are some questions:\n":
            ask_questions()

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
