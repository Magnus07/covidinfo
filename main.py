import telebot
from telebot import types
import requests
import os
import json

covid_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/random_masks_usage_instructions.php"
geo_url   = "https://geocodeapi.p.rapidapi.com/GetNearestCities"
querystring = {"latitude":"","longitude":"","range":"0"}
headers = {
    'x-rapidapi-host': "geocodeapi.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
}

country_by_name_url = "https://coronavirus-monitor.p.rapidapi.com/coronavirus/cases_by_country.php"
country_by_name_headers = {
    'x-rapidapi-host': "coronavirus-monitor.p.rapidapi.com",
    'x-rapidapi-key': "e0148a3467msh96216911de4311bp11d63djsn470777193a84"
}

def nameApiRequest(url, headers):
    return requests.request("GET", url, headers=headers)

def apiRequest(url, headers, params):
    return requests.request("GET", url, headers=headers, params=params)

bot = telebot.TeleBot(os.environ.get("API"))
@bot.message_handler(commands=['start'])
def start_message(message):
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
	querystring["latitude"] = message.location.latitude
	querystring["longitude"] = message.location.longitude
	response = apiRequest(geo_url,headers,querystring).text
	jsoned = json.loads(response)
	bot.send_message(message.chat.id, jsoned[0]["Country"])
	#я говорил тебе об этой функции, обнови

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