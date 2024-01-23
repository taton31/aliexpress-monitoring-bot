from app import bot
from app import get_users, save_users

from telebot import types

users = get_users()
# {1234324: {'name': {'url': 'asdf', 'history': [11,22,33]}}}

@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), commands=['config'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    
    global users
    users = get_users()
    for key, value in users[str(message.chat.id)]['products'].items():
        markup.add(types.InlineKeyboardButton(key, callback_data=f'config:{key}'))
    
    bot.delete_state(message.chat.id)
    bot.send_message(message.chat.id, "Ваши отслеживаемые позиции. Нажмите, чтобы удалить:", reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith('config:') and str(call.message.chat.id) in users.keys())
def send_admin_request(call):

    global users
    users = get_users()
    users[str(call.message.chat.id)]['products'].pop(call.data.split(':')[1], 0)
    save_users(users)
    bot.send_message(call.message.chat.id, 'Удалено')
    bot.answer_callback_query(call.id)

