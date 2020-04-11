import telebot
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
    bot.send_message(message.chat.id, 'Получать статистику по названию или координатам?')
		
@bot.message_handler(content_types=['text'])
def get_info_by_location(message):
	country_cases = nameApiRequest(country_by_name_url, country_by_name_headers)
	jsoned = json.loads(country_cases.text)
	found=0
	for x in jsoned['countries_stat']:
		if (x['country_name']==message.text):
			bot.send_message(message.chat.id, "В стране "+message.text+
			"\nЗаражено: "+x['cases']+"\nПогибло: "+x['deaths']+"\nВыздоровело: "+x['total_recovered']+
			"\nВ тяжелом состоянии: "+x['serious_critical']+"\n\nНовые случаи:\nЗаражено: "+x['new_cases']+"\nПогибло: "+x['new_deaths'])
			found=1
	if(found==0):
		bot.send_message(message.chat.id, "К сожалению, не найдено информации о стране "+message.text)

    
@bot.message_handler(content_types=['location'])
def get_info_by_location(message):
    querystring["latitude"] = message.location.latitude
    querystring["longitude"] = message.location.longitude
    response = apiRequest(geo_url,headers,querystring).text
    jsoned = json.loads(response)

    bot.send_message(message.chat.id, jsoned[0]["Country"])


bot.polling()