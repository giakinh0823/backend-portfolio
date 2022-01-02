#app/__init__.py
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

__all__ = ('celery_app',)


# from chatbot.chatbot import bot
# from chatterbot.trainers import ListTrainer
# from chatterbot.trainers import ChatterBotCorpusTrainer

# trainer = ChatterBotCorpusTrainer(bot.chatbot)

# trainer.train(
#     "chatterbot.corpus.english",
# )

# list_trainer = ListTrainer(bot.chatbot)

# list_trainer.train([
#     "Hi",
#     "Chào bạn! Tôi là trợ lý ảo của Hà Gia Kính. Tôi có thể giúp gì cho bạn?",
#     "What is your name",
#     "My name is Noki-bot",
#     "How old are you?",
#     "Tôi mới được 1 tuổi",
#     "Hey",
#     "What's up?",
#     "How are you doing",
#     "Tôi đang nói chuyện với bạn. Và tôi rất phấn khích vì đều đó",
#     "What is your favorite color?",
#     "Tôi yêu màu mà bạn đã chọn cho tôi trong trang web của tôi",
# ])


# list_trainer.train([
#     "cc",
#     "Bạn không được phép chửi tôi",
#     "cunt",
#     "Fuck you",
#     "cock",
#     "Bạn có không? Liệu nó có lớn hơn tôi không",
#     "lz",
#     "Bạn nói bậy rồi đấy ? Tôi về bảo với mẹ bạn.!"
#     "Fuck your mother",
#     "Fuck your dad",
#     "Fuck you",
#     "Fuck your mother",
# ])
