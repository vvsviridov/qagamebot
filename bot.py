import os
import telebot
from telebot import types
from text import questions, answers
from random import shuffle
from flask import Flask, request


TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

shuffle(answers)
shuffle(questions)


@bot.inline_handler(lambda query: query.query.lower() == 'вопрос')
def question_text(inline_query):
    try:
        resp = types.InlineQueryResultArticle(
            '1',
            'Вопрос',
            types.InputTextMessageContent(questions.pop())
        )
        bot.answer_inline_query(inline_query.id, [resp], cache_time=0)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query.lower() == 'ответ')
def answer_text(inline_query):
    try:
        resp = types.InlineQueryResultArticle(
            '1',
            'Ответ',
            types.InputTextMessageContent(answers.pop())
        )
        bot.answer_inline_query(inline_query.id, [resp], cache_time=0)
    except Exception as e:
        print(e)


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://qagame-telegram.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
