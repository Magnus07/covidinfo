import telebot
import pymongo
from telebot import types
import requests
import os
import json


client     = pymongo.MongoClient(os.environ.get("MONGODB"))
db         = client.test_database
collection = db.test_collection
users = db.users

user = {
    "name" : "",
    "city" : "",
    "adress" : ""
}

bot = telebot.TeleBot(os.environ.get("API"))

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