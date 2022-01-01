#app/__init__.py
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

__all__ = ('celery_app',)


from chatbot.chatbot import bot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

trainer = ChatterBotCorpusTrainer(bot.chatbot)

trainer.train(
    "chatterbot.corpus.english",
)

list_trainer = ListTrainer(bot.chatbot)

list_trainer.train([
    "Hi",
    "Chào bạn! Tôi là trợ lý ảo của Hà Gia Kính. Tôi có thể giúp gì cho bạn?",
    "What is your name?",
    "My name is Giakinh-bot",
    "How old are you?",
    "Tôi mới được 1 tuổi",
])




