import os

import telebot
from flask import Flask, request
from telebot import TeleBot

from config import TOKEN
from libs import send_wide_video

bot = TeleBot(TOKEN)


@bot.message_handler(content_types=["video"])
def video_test(m):
    print(m)
    send_wide_video(bot, m.chat.id, m.video)


@bot.message_handler(content_types=["document"],
                     func=lambda m: m.document and m.document.mime_type in ["image/gif",
                                                                            "video/mpeg",
                                                                            "video/mp4",
                                                                            "video/ogg",
                                                                            "video/webm"])
def doc_video(m):
    print(m)
    send_wide_video(bot, m.chat.id, m.document)


@bot.message_handler()
def all(m):
    bot.send_message(m.chat.id, "🎞️ Please, send me a video or a gif")


if "webhooks" in list(os.environ.keys()):
    server = Flask(__name__)


    @server.route(f"/{TOKEN}", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=os.environ["app_url"] + TOKEN)
        return "!", 200


    server.run(host="0.0.0.0", port=os.environ.get('port', 5000))

else:
    bot.remove_webhook()
    bot.polling()
