import telebot
import requests
import os

import requests

url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/random_masks_usage_instructions.php"

headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

bot = telebot.TeleBot(os.environ.get("API"))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Получать погоду по названию или координатам?')

bot.polling()