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
from ChatBot.load_questions import subjects

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)


def train_subject_prompts(bot):
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


def createChatbot():
    db_exists = os.path.exists("../Data/database.db")

    # Create a new instance of a ChatBot
    bot = ChatBot(
        "MCATutor",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
            "chatterbot.logic.TimeLogicAdapter",
            "chatterbot.logic.BestMatch"
        ],
        input_adapter="chatterbot.input.VariableInputTypeAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        database="../Data/database"
    )

    if not db_exists:
        bot.set_trainer(ChatterBotCorpusTrainer)
        bot.train("chatterbot.corpus.english")
        bot.train("chatterbot.corpus.english.greetings")

        bot.set_trainer(ListTrainer)
        train_subject_prompts(bot)

    return bot
