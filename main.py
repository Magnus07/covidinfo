import telebot
import requests
import os
import json

import requests

covid_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/random_masks_usage_instructions.php"
geo_url   = "https://geocodeapi.p.rapidapi.com/GetNearestCities"

querystring = {"latitude":"","longitude":"","range":"0"}

headers = {
    'x-rapidapi-host': "geocodeapi.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
}


def apiRequest(url, headers, params):
    return requests.request("GET", url, headers=headers, params=params)

# response = requests.request("GET", url, headers=headers)

# print(response.text)

bot = telebot.TeleBot(os.environ.get("API"))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Получать погоду по названию или координатам?')

@bot.message_handler(content_types=['location'])
def get_info_by_location(message):
    querystring["latitude"] = message.location.latitude
    querystring["longitude"] = message.location.longitude
    response = apiRequest(geo_url,headers,querystring).text
    jsoned = json.loads(response)

    bot.send_message(message.chat.id, jsoned[0]["Country"])


bot.polling()