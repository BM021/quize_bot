import telebot

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import database
import buttons

TOKEN = '6547849200:AAEIzUzuj6eGp8to4X-h8TIobO66fVMX4YM'

bot = telebot.TeleBot(TOKEN)

user_answers = {}

questions = [
    {
        'question': 'Python bu',
        'options': ['Frontend tili', 'Dasturlash tili', 'Ona tili'],
        'correct_option': 1
    },
    {
        'question': 'Pythonda neshta malumot turi bor?',
        'options': ['7', '5', '2', '9'],
        'correct_option': 0
    },
    {
        'question': 'Python qaysi tili?',
        'options': ['frontend', 'full stack', 'backend'],
        'correct_option': 2
    },
    {
        'question': 'Pythonda class nomine qanaqa beriladi?',
        'options': ['class Car:', 'class:', 'def'],
        'correct_option': 0
    },
    {
        'question': 'Pythonda funksiya qanaqa yaratiladi?',
        'options': ['def name()', 'name()', 'def name():'],
        'correct_option': 2
    }
]


@bot.message_handler(commands=['start'])
def start(message):

    checker = database.check_user(message.from_user.id)

    if checker:
        bot.send_message(message.from_user.id, 'TO START GAME PRESS THE BUTTON')  # start game button

    else:
        bot.send_message(message.from_user.id, 'Share your contact to play game')  # contact button
        bot.register_next_step_handler(message, get_contact)


def get_contact(message):
    if message.contact:
        user_phone = message.contact.phone_number
        first_name = message.contact.first_name

        database.register_user(first_name, message.from_user.id, user_phone)

        bot.send_message(message.from_user.id, 'You registered successfully')  # start game button

    else:
        bot.send_message(message.from_user.id, 'Please to share contact user the button')  # contact button
        bot.register_next_step_handler(message, get_contact)


@bot.message_handler(content_types=['text'])
def start_game(message):
    if message.text.lower() == 'start game':

        user_answers[message.from_user.id] = []
        start_the_game(message, message.from_user.id, 0)


def start_the_game(message, telegram_id, question_index):
    if question_index < len(questions):
        question_data = questions[question_index]
        question_text = question_data['question']
        question_options = question_data['options']

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for option in question_options:
            markup.add(KeyboardButton(option))

        bot.send_message(telegram_id, question_text, reply_markup=markup)
        bot.register_next_step_handler(message, check_answer, telegram_id, question_data)

    else:

        result = user_answers[telegram_id].count(True)
        bot.send_message(telegram_id, f'Your result is {len(questions)}/{result} correct', reply_markup=buttons.start_game())


def check_answer(message, telegram_id, question_data):
    user_answer = message.text
    correct_answer = question_data['correct_option']

    if user_answer == question_data['options'][correct_answer]:
        user_answers[telegram_id].append(True)

    else:
        user_answers[telegram_id].append(False)

    next_question_index = len(user_answers[telegram_id])
    start_the_game(message, telegram_id, next_question_index)


bot.polling()
