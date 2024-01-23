from app import bot, States
from app import get_users, save_users
from app import get_price

import time
from telebot import types


users = get_users()

def list_to_string(input_list):
    return '\n'.join(map(str, input_list))

@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), commands=['prices'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    
    refresh_prises = types.InlineKeyboardButton("Обновить все цены", callback_data='refresh_prises')
    show_prises = types.InlineKeyboardButton("Показать цены", callback_data='show_prises')
    markup.add(refresh_prises, show_prises)

    bot.send_message(message.chat.id, "Что хочешь? \nДля добавления товара отправь ссылку", reply_markup=markup)
    bot.set_state(message.chat.id, States.prices)


# {1234324: {'name': {'url': 'asdf', 'history': [11,22,33]}}}

@bot.callback_query_handler(func=lambda call: call.data == 'refresh_prises', state=States.prices)
def send_admin_request(call):
    global users
    users = get_users()
    for product in users[str(call.message.chat.id)]['products'].keys():
        price = get_price( users[str(call.message.chat.id)]['products'][product]['url'] )
        users[str(call.message.chat.id)]['products'][product]['history'] = users[str(call.message.chat.id)]['products'][product]['history'][-9:] + [price]
        bot.send_message(call.message.chat.id, "Запрашиваю, ждите")
        time.sleep(1)
    save_users(users)

    bot.send_message(call.message.chat.id, "Готово")
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data == 'show_prises', state=States.prices)
def send_admin_request(call):
    global users
    users = get_users()
    for product in users[str(call.message.chat.id)]['products'].keys():

        # users[str(call.message.chat.id)]['products'][product]['history'] = users[str(call.message.chat.id)]['products'][product]['history']
        bot.send_message(call.message.chat.id, f"{product}:\n{list_to_string(users[str(call.message.chat.id)]['products'][product]['history'])}")

    bot.answer_callback_query(call.id)






@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys() and message.text.startswith('https://aliexpress.ru/item/'), state=States.prices)
def start(message):
    bot.send_message(message.chat.id, "Введи название")
    
    bot.register_next_step_handler_by_chat_id(message.chat.id, name_to_product, (message.text, ))





def name_to_product(message, url):
    global users
    users = get_users()
    users[str(message.chat.id)]['products'][message.text] = {'url': url[0], 'history': []}
    save_users(users)
    bot.send_message(message.chat.id, "Сохранено")




@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys() and not message.text.startswith('https://aliexpress.ru/item/'), state=States.prices)
def start(message):
    bot.send_message(message.chat.id, "Не похоже на ссылку на товар")
