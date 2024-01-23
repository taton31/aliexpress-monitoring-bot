from app import bot, States
from app import get_request_users, save_request_users, get_users

from telebot import types

users = get_users()
request_users = get_request_users()

def get_inline_keyboard_markup():
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton("Да", callback_data='yes')
    button_no = types.InlineKeyboardButton("Нет", callback_data='no')
    markup.add(button_yes, button_no)
    return markup


@bot.message_handler(func=lambda message: str(message.chat.id) not in users.keys() and message.chat.id not in request_users.keys(), commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Нужно зарегистрироваться, отправить запрос админу?", reply_markup=get_inline_keyboard_markup())
    bot.set_state(message.chat.id, States.new_user)

    # bot.register_next_step_handler_by_chat_id(message.chat.id, send_admin_request)

@bot.callback_query_handler(func=lambda call: True, state=States.new_user)
def send_admin_request(call):
    if call.data == 'yes':
        global request_users
        request_users[call.message.chat.id] = call.message.chat.first_name if call.message.chat.first_name else 'Не известно'
        save_request_users(request_users)

        bot.send_message(call.message.chat.id, "Запрос отправлен")
    else:        
        bot.send_message(call.message.chat.id, "Как хочешь")

    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: str(message.chat.id) not in users.keys() and message.chat.id in request_users.keys(), commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Запрос отправлен, жди")


@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ты уже имеешь доступ")