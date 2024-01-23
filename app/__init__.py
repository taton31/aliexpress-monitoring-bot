import telebot
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters

from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage() 

class States(StatesGroup):
    new_user = State() 
    admin = State()
    prices = State()


bot = telebot.TeleBot('6751865052:AAEmhfA__sQTomRIgFP7S3VBz5aPGwfWWCY', state_storage=state_storage)

from aliexpress_parse import get_price
from db.files import get_admins, save_admins, get_users, save_users, get_request_users, save_request_users


from app.handlers import new_user, admin, config, prices, error

bot.add_custom_filter(custom_filters.StateFilter(bot))