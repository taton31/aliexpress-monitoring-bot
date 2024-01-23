from app import bot

@bot.message_handler()
def start(message):
    bot.send_message(message.chat.id, "Не поняль")
