from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.logic import LogicAdapter
from chatterbot.trainers import ListTrainer
from .models import Message, Group

import en_core_web_sm
import spacy
en_core_web_sm.load()
spacy.load('en_core_web_sm')
spacy.load('en')


class Chatbot:
    def __init__(self):
        self.chatbot = ChatBot(**settings.CHATTERBOT)

    def get_response(self, text):
        bot_response = self.chatbot.get_response(text)
        return bot_response

    def train(self):
        list_trainer = ListTrainer(self.chatbot)
        groups = Group.objects.all()
        for group in groups:
            list_message = []
            messages = Message.objects.filter(group=group).order_by('-created_at')
            for message in messages:
                list_message.append(str(message.message))
            list_trainer.train(list_message)


bot = Chatbot()


class LogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, input_statement, statement_list, storage=None):
        import random

        # Randomly select a confidence between 0 and 1
        confidence = random.uniform(0, 1)

        # For this example, we will just return the input as output
        selected_statement = input_statement
        selected_statement.confidence = confidence

        return selected_statement
