import os
import telebot
import time
from telebot import types
from text import questions, answers
from random import shuffle

TELEGRAM_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TELEGRAM_TOKEN)
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


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
