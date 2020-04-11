import telebot
import pymongo
from telebot import types
import requests
import os
import json


client     = pymongo.MongoClient(os.environ.get("MONGODB"))
db         = client.test_database
collection = db.test_collection

user = {
    "name" : "",
    "adress" : ""
}

covid_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/random_masks_usage_instructions.php"
covid_country_by_name = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/latest_stat_by_country.php"
geo_url   = "https://geocodeapi.p.rapidapi.com/GetNearestCities"

locationstring = {"latitude":"","longitude":"","range":"0"}

querystring = {"latitude":"","longitude":"","range":"0"}

headers = {
    'x-rapidapi-host': "geocodeapi.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
}

bot = telebot.TeleBot(os.environ.get("API"))

def get_headers(host):
    headers["x-rapidapi-host"]=host
    return headers

country_by_name_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"
country_by_name_headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
}

def nameApiRequest(url, headers):
    return requests.request("GET", url, headers=headers)

def apiRequest(url, headers, params):
    return requests.request("GET", url, headers=headers, params=params).text


def make_string(caption,data):
    return caption + " : " + data + "\n"


def get_stat_by_country(country):
    response = apiRequest(covid_country_by_name, headers = get_headers("coronavirus-monitor.p.rapidapi.com"),params = {"country" : country})
    jsoned = json.loads(response)

    message = make_string("Обрана країна",jsoned["latest_stat_by_country"][0]["country_name"]) + make_string(" Усього випадків захворювання",jsoned["latest_stat_by_country"][0]["total_cases"]) + make_string(" За минулу добу" ,jsoned["latest_stat_by_country"][0]["new_cases"]) + make_string("Активні випадки",jsoned["latest_stat_by_country"][0]["active_cases"])+ make_string("Усього смертей",jsoned["latest_stat_by_country"][0]["total_deaths"])+ make_string("Смертей за останню добу",jsoned["latest_stat_by_country"][0]["new_deaths"])+ make_string("Усього видужаних",jsoned["latest_stat_by_country"][0]["total_recovered"])+ make_string("У критичному стані",jsoned["latest_stat_by_country"][0]["serious_critical"]) + make_string("Дата",jsoned["latest_stat_by_country"][0]["record_date"])
    return message


bot = telebot.TeleBot(os.environ.get("API"))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Получать статистику по названию или координатам?')


def save_adress(message):
    users = db.users
    user["adress"] = message.text
    users.insert_one(user)
    bot.send_message(message.from_user.id, "Інформація збережена")

def enter_adress(message):
    msg = bot.send_message(message.from_user.id, "Укажіть адресу")
    user["name"] = message.text
    bot.register_next_step_handler(msg,save_adress)

@bot.message_handler(commands=['inform'])
def handle_start(message):
    msg = bot.send_message(message.from_user.id, "Уведіть своє ім'я та прізвище: ")
    bot.register_next_step_handler(msg,enter_adress)
		
    keyboard_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard_markup.row('Пошук за назвою країни', 'Пошук за назвою міста')
    keyboard_markup.row('Пошук по координатам', 'Додати інформацію про випадок зараження')
    bot.send_message(message.chat.id, 'Яким чином ви бажаєте взаємодіяти з ботом?', reply_markup=keyboard_markup)


@bot.message_handler(content_types=['text'])
def get_info_by_location(message):
	if(message.text=="Пошук за назвою країни"):
		bot.send_message(message.chat.id, "Введіть назву країни")
		bot.register_next_step_handler(message, by_country_name)
	elif(message.text=="Пошук за назвою міста"):
		bot.send_message(message.chat.id, "Введіть назву міста")
		bot.register_next_step_handler(message, by_city_name)
	elif(message.text=="Пошук по координатам"):
		bot.send_message(message.chat.id, "Відправте свої координати")
		bot.register_next_step_handler(message, by_coordinates)
	elif(message.text=="Додати інформацію про випадок зараження"):
		bot.send_message(message.chat.id, "Дайте детальний опис ситуації")
		bot.register_next_step_handler(message, add_covid_case)

def by_coordinates(message):
    locationstring["latitude"] = message.location.latitude
    locationstring["longitude"] = message.location.longitude
    response = apiRequest(geo_url,get_headers("geocodeapi.p.rapidapi.com"),locationstring)
    jsoned = json.loads(response)

    bot.send_message(message.chat.id, get_stat_by_country(jsoned[0]["Country"]))

def by_country_name(message):
	country_cases = nameApiRequest(country_by_name_url, country_by_name_headers)
	jsoned = json.loads(country_cases.text)
	found=0
	for x in jsoned['countries_stat']:
		if (x['country_name']==message.text):
			bot.send_message(message.chat.id, "В країні "+message.text+
			"\nІнфікованих: "+x['cases']+"\nЗагинуло: "+x['deaths']+"\nОдужало"+x['total_recovered']+
			"\nВ тяжкому стані: "+x['serious_critical']+"\n\nНові випадки:\nІнфікованих: "+x['new_cases']+"\nЗагинуло: "+x['new_deaths'])
			found=1
	if(found==0):
		bot.send_message(message.chat.id, "На жаль, не має інформації про країну "+message.text)
            

def by_city_name(message):
	bot.send_message(message.chat.id, "...")
	#просто затычка для поиска по городу

def add_covid_case(message):
	bot.send_message(message.chat.id, "...")
	#просто затычка для добавления нового случая
bot.polling()