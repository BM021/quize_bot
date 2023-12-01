import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('6687639473:AAHaH-U8ykafItr5oMYREXryynNrCyI0nNc')

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


def phone_button():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    button = KeyboardButton('share contact', request_contact=True)

    kb.add(button)

    return kb




@bot.message_handler(commands=['start'])
def start_message(message):
    
    text = f'Hello {message.from_user.first_name}!\nWelcome to quize bot, here you can win sweets and other things\nSend me your name to start the game.'

    bot.send_message(message.from_user.id, text)
    bot.register_next_step_handler(message, get_name)



def get_name(message):
    user_name = message.text

    bot.send_message(message.from_user.id, 'Share your contact', reply_markup=phone_button())
    bot.register_next_step_handler(message, get_contact, user_name)


def get_contact(message, user_name):
    if message.contact:
        user_phone = message.contact.phone_number

        bot.send_message(message.from_user.id, 'Well done, the game will start in 5 seconds')

    else:
        bot.send_message(message.from_user.id, 'Use the button to share your contact')
        bot.register_next_step_handler(message, get_contact, user_name)



@bot.message_handler(content_types=['text'])
def game(message):
    if message.text.lower() == 'start game':

        user_answers[message.from_user.id] = []
        start_game(message, message.from_user.id, 0)



def start_game(message, user_id, question_index):
    if question_index < len(questions):
        question_data = questions[question_index]
        question_text = question_data['question']
        question_options = question_data['options']

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for option in question_options:
            markup.add(KeyboardButton(option))

        bot.send_message(user_id, question_text, reply_markup=markup)
        bot.register_next_step_handler(message, check_answer, user_id, question_data)

    else:

        score = 0
        for i in user_answers[user_id]:
            if i == True:
                score = score + 1

        bot.send_message(user_id, f'Siz 10 tadan {score} tori topdis')



def check_answer(message, user_id, question_data):
    user_answer = message.text
    correct_answer = question_data['correct_option']

    if user_answer == question_data['options'][correct_answer]:
        user_answers[user_id].append(True)

    else:
        user_answers[user_id].append(False)

    question_next_index = len(user_answers[user_id])
    start_game(message, user_id, question_next_index)



bot.polling()
