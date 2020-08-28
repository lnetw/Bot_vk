import requests
from bs4 import BeautifulSoup
from translate import Translator
import re
import datetime

regular = re.compile(r'>(.+){1,20}<')


def weather_forecast(city, date, context, flag):
    translator = Translator(from_lang="russian", to_lang="english")
    translation_city = translator.translate(city)
    url = f'https://yandex.ru/pogoda/{translation_city}'
    page = requests.get(url=url)
    html_page = BeautifulSoup(page.text, features='html.parser')
    temperature = html_page.find_all('span', {'class': 'temp__value'})
    condition = html_page.find_all('div', {'class': 'forecast-briefly__condition'})
    if flag == 0:
        day_forecast = datetime.datetime.strptime(date, "%d-%m-%Y").date()
        today = datetime.datetime.today().date()
        result_day = day_forecast - today
        i = int(result_day.days) + 1
    elif date == 'вчера':
        i = 0
    elif date == 'сегодня':
        i = 1
    elif date == 'завтра':
        i = 2
    else:
        return False
    match_temp = re.search(regular, str(temperature[i * 2 + 9]))
    match_condition = re.search(regular, str(condition[i + 3]))
    context['condition'] = str(match_condition[1]).lower()
    context['temperature'] = match_temp[1]
    return True