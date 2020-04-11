from config import *


def get_stat_by_country(country):
    response = apiRequest(covid_country_by_name, headers = get_headers("coronavirus-monitor.p.rapidapi.com"),params = {"country" : country})
    jsoned = json.loads(response)
    message = make_string("Обрана країна",jsoned["latest_stat_by_country"][0]["country_name"]) + make_string(" Усього випадків захворювання",jsoned["latest_stat_by_country"][0]["total_cases"]) + make_string(" За минулу добу" ,jsoned["latest_stat_by_country"][0]["new_cases"]) + make_string("Активні випадки",jsoned["latest_stat_by_country"][0]["active_cases"])+ make_string("Усього смертей",jsoned["latest_stat_by_country"][0]["total_deaths"])+ make_string("Смертей за останню добу",jsoned["latest_stat_by_country"][0]["new_deaths"])+ make_string("Усього видужаних",jsoned["latest_stat_by_country"][0]["total_recovered"])+ make_string("У критичному стані",jsoned["latest_stat_by_country"][0]["serious_critical"]) + make_string("Дата",jsoned["latest_stat_by_country"][0]["record_date"])
    return message


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard_markup.row('Пошук за назвою країни', 'Пошук за містом')
    keyboard_markup.row('Пошук по координатам', 'Додати інформацію про випадок зараження')
    bot.send_message(message.chat.id, 'Яким чином ви бажаєте взаємодіяти з ботом?', reply_markup=keyboard_markup)


def save_adress(message):
    user["adress"] = message.text
    users.insert_one(user)
    bot.send_message(message.from_user.id, "Інформація збережена")


def enter_adress(message):
    msg = bot.send_message(message.from_user.id, "Укажіть адресу")
    user["city"] = message.text
    bot.register_next_step_handler(msg,save_adress)


def enter_city(message):
    msg = bot.send_message(message.from_user.id, "Укажіть місто")
    user["name"] = message.text
    bot.register_next_step_handler(msg,enter_adress)


@bot.message_handler(content_types=['text'])
def get_info_by_location(message):
	if(message.text=="Пошук за назвою країни"):
		bot.send_message(message.chat.id, "Введіть назву країни")
		bot.register_next_step_handler(message, by_country_name)
	elif(message.text=="Пошук за містом"):
		bot.send_message(message.chat.id, "Введіть місто")
		bot.register_next_step_handler(message, by_city_name)
	elif(message.text=="Пошук по координатам"):
		bot.send_message(message.chat.id, "Відправте свої координати")
		bot.register_next_step_handler(message, by_coordinates)
	elif(message.text=="Додати інформацію про випадок зараження"):
		bot.send_message(message.chat.id, "Уведіть ім'я та прізвище: ")
		bot.register_next_step_handler(message, enter_city)


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
			"\nІнфікованих: "+x['cases']+"\nЗагинуло: "+x['deaths']+"\nОдужало:"+x['total_recovered']+
			"\nВ тяжкому стані: "+x['serious_critical']+"\n\nНові випадки:\nІнфікованих: "+x['new_cases']+"\nЗагинуло: "+x['new_deaths'])
			found=1
	if(found==0):
		bot.send_message(message.chat.id, "На жаль, не має інформації про країну "+str(message.text))


def by_city_name(message):
    result = ""
    for user in users.find({"city": message.text}):
       result += user["name"] + ",м." + user["city"] + "," + user["adress"] + "\n"
    if result == "":
        bot.send_message(message.chat.id, "Дані про випадки захворювання в місті відсутні.")
    else:
	    bot.send_message(message.chat.id, "Ідентифіковані захворюванні: \n" + result)

bot.polling()