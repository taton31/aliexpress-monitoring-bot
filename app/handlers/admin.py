from app import bot, States
from app import get_admins, save_admins, get_request_users, save_request_users, get_users, save_users

from telebot import types

admins = get_admins()
users = get_users()

def get_inline_keyboard_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    add_user = types.InlineKeyboardButton("Заявки на добавление к боту", callback_data='add_user')
    delete_user = types.InlineKeyboardButton("Удаление пользователей", callback_data='remove_user')
    # button_no = types.InlineKeyboardButton("Нет", callback_data='no')
    markup.add(add_user, delete_user)
    return markup


@bot.message_handler(func=lambda message: str(message.chat.id) not in users.keys(), commands=['admin'])
def start(message):
    bot.send_message(message.chat.id, 'Ты не можешь быть админом')



@bot.message_handler(func=lambda message: message.chat.id not in admins, commands=['admin'])
def start(message):
    bot.send_message(message.chat.id, "Ты не админ. Для авторизации введи логин")

    bot.register_next_step_handler_by_chat_id(message.chat.id, admin_auth_log)


def admin_auth_log(message):
    bot.send_message(message.chat.id, "Теперь пароль")

    if message.text == 'fynjy15456':
        bot.register_next_step_handler_by_chat_id(message.chat.id, admin_auth_log_correct)
    else:        
        bot.register_next_step_handler_by_chat_id(message.chat.id, admin_auth_log_correct)


def admin_auth_log_correct(message):
    if message.text == 'fynjy15456':
        bot.send_message(message.chat.id, "Теперь ты админ\nУрааааа")

        global admins
        admins = get_admins()
        admins.add(message.chat.id)
        save_admins(admins)
        bot.set_state(message.chat.id, States.admin)

    else:        
        bot.send_message(message.chat.id, "Неверный логин или пароль")


def admin_auth_log_incorrect(message):
    bot.send_message(message.chat.id, "Неверный логин или пароль")



@bot.message_handler(func=lambda message: message.chat.id in admins, commands=['admin'])
def start(message):
    bot.send_message(message.chat.id, "Что хочешь?", reply_markup=get_inline_keyboard_markup())
    bot.set_state(message.chat.id, States.admin)

    # bot.register_next_step_handler_by_chat_id(message.chat.id, send_admin_request)

@bot.callback_query_handler(func=lambda call: call.data == 'add_user', state=States.admin)
def send_admin_request(call):
    global request_users
    request_users = get_request_users()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1


    for key, value in request_users.items():
        markup.add(types.InlineKeyboardButton(f'{key}: {value}', callback_data=f'add_user:{key}:{value}'))
    
    if not request_users:
        bot.send_message(call.message.chat.id, "Все добавлены")
    else:
        bot.send_message(call.message.chat.id, "Кого добавим?", reply_markup=markup)

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_user:'), state=States.admin)
def send_admin_request(call):
    adding_user = int(call.data.split(':')[1])
    adding_user_name = call.data.split(':')[2]

    global request_users
    request_users = get_request_users()
    request_users.pop(adding_user, None)
    save_request_users(request_users)

    global users
    users = get_users()
    users[str(adding_user)] = {'name': adding_user_name}
    users[str(adding_user)] = {'products': {}}
    save_users(users)

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1

    for key, value in request_users.items():
        markup.add(types.InlineKeyboardButton(f'{key}: {value}', callback_data=f'add_user:{key}:{value}'))
    
    if not request_users:
        bot.send_message(call.message.chat.id, "Все добавлены")
    else:
        bot.send_message(call.message.chat.id, "Кого еще добавим?", reply_markup=markup)
    

    bot.answer_callback_query(call.id)



@bot.callback_query_handler(func=lambda call: call.data == 'remove_user', state=States.admin)
def send_admin_request(call):
    global users
    users = get_users()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    a = dict()
    for key, value in users.items():
        markup.add(types.InlineKeyboardButton(f'{key}: {value.get("name", "None")}', callback_data=f'remove_user:{key}'))
    
    bot.send_message(call.message.chat.id, "Кого удалим?", reply_markup=markup)

    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('remove_user:'), state=States.admin)
def send_admin_request(call):
    removing_user = int(call.data.split(':')[1])

    global admins
    admins = get_admins()
    admins.discard(removing_user)
    save_admins(admins)

    global users
    users = get_users()
    users.pop(str(removing_user), None)
    save_users(users)

    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1

    for key, value in users.items():
        markup.add(types.InlineKeyboardButton(f'{key}: {value.get("name", "None")}', callback_data=f'remove_user:{key}'))
    
    bot.send_message(call.message.chat.id, "Кого еще удалим?", reply_markup=markup)

    bot.answer_callback_query(call.id)



