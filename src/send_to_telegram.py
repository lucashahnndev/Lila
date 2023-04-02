import json
import telebot
from debug import log

file_config = open('data/config.json', 'r')
config = json.load(file_config)
bot = telebot.TeleBot(config["telegram"]["botkey"])

def send_to_telegram(id_user, mensagem):
    try:
        bot.send_message(id_user, mensagem)
    except Exception as error:
        log(error, 'tmp/log.log')
        bot.send_message(id_user, f"Desculpe me, ouve um erro")