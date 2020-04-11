import telebot
import requests
import os
import json

import requests

covid_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/random_masks_usage_instructions.php"
covid_country_by_name = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
geo_url   = "https://geocodeapi.p.rapidapi.com/GetNearestCities"

locationstring = {"latitude":"","longitude":"","range":"0"}

headers = {
    'x-rapidapi-host': "geocodeapi.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
}

bot = telebot.TeleBot(os.environ.get("API"))

def get_headers(host):
    headers["x-rapidapi-host"]=host
    return headers


def apiRequest(url, headers, params):
    return requests.request("GET", url, headers=headers, params=params).text

def make_string(caption,data):
    return caption + " : " + data + "\n"


def get_stat_by_country(country):
    response = apiRequest(covid_country_by_name, headers = get_headers("coronavirus-monitor.p.rapidapi.com"),params = {"country" : country})
    jsoned = json.loads(response)

    message = make_string("Обрана країна",jsoned["latest_stat_by_country"][0]["country_name"]) + make_string(" Усього випадків захворювання",jsoned["latest_stat_by_country"][0]["total_cases"]) + make_string(" За минулу добу" ,jsoned["latest_stat_by_country"][0]["new_cases"]) + make_string("Активні випадки",jsoned["latest_stat_by_country"][0]["active_cases"])+ make_string("Усього смертей",jsoned["latest_stat_by_country"][0]["total_deaths"])+ make_string("Смертей за останню добу",jsoned["latest_stat_by_country"][0]["new_deaths"])+ make_string("Усього видужаних",jsoned["latest_stat_by_country"][0]["total_recovered"])+ make_string("У критичному стані",jsoned["latest_stat_by_country"][0]["serious_critical"]) + make_string("Дата",jsoned["latest_stat_by_country"][0]["record_date"])
    return message

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Получать погоду по названию или координатам?')

@bot.message_handler(content_types=['location'])
def get_info_by_location(message):
    locationstring["latitude"] = message.location.latitude
    locationstring["longitude"] = message.location.longitude
    response = apiRequest(geo_url,get_headers("geocodeapi.p.rapidapi.com"),locationstring)
    jsoned = json.loads(response)

    bot.send_message(message.chat.id, get_stat_by_country(jsoned[0]["Country"]))


bot.polling()