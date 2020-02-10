import os
import telebot
from telebot import types
from text import questions, answers
from random import shuffle
from flask import Flask, request


TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


query_answers = []
query_questions = []


def shuffle_answers():
    shuffle(answers)
    return answers.copy()


def shuffle_questions():
    shuffle(questions)
    return questions.copy()


@bot.inline_handler(lambda query: query.query.lower() == '')
def question_text(inline_query):
    global query_questions
    global query_answers
    try:
        if len(query_questions) == 0:
            query_questions = shuffle_questions()
        if len(query_answers) == 0:
            query_answers = shuffle_answers()
        resp1 = types.InlineQueryResultArticle(
            '1',
            'Спросить',
            types.InputTextMessageContent(query_questions.pop())
        )
        resp2 = types.InlineQueryResultArticle(
            '2',
            'Ответить',
            types.InputTextMessageContent(query_answers.pop())
        )
        bot.answer_inline_query(inline_query.id, [resp1, resp2], cache_time=0)
    except Exception as e:
        print(e)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://qagame-telegram.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
