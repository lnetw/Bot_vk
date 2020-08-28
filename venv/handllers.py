import re
from generate_image import generate_cats
from weather_forecast import weather_forecast
import random

# Регулярные выражения для ивентов бота
regular_name = re.compile(r'^[\D\-\s]{3,20}$')
regular_number = re.compile(r'\b[\d]{1,2}\b')
regular_city = re.compile(r'^[а-яА-Я]+$')
list_date = ['вчера', 'сегодня', 'завтра']
regular_date = re.compile(r'(?<!\d)(?:0[1-9]|[12][0-9]|3[01])-(?:0[0-9]|1[0-2])-(?:19[0-9][0-9]|20[012][0-9])(?!\d)')


# Функции реализации ивентов бота
def handle_name(text, context):
    match = re.match(regular_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handle_surname(text, context):
    match = re.match(regular_name, text)
    if match:
        context['surname'] = text
        return True
    else:
        return False


def handle_city(text, context):
    match = re.match(regular_city, text)
    if match:
        context['city'] = str(text)[:1].upper() + str(text)[1:]
        return True
    else:
        return False


def handle_weather(text, context):
    flag = 1
    match = re.match(regular_date, text)
    if match:
        context['date'] = text
        if weather_forecast(context['city'], text, context, flag=0):
            return True
    elif str(text) in list_date:
        context['date'] = text
        if weather_forecast(context['city'], text, context, flag=1):
            return True
    else:
        return False


def handler_generate_image(text, context):
    return generate_cats()


def handle_game_begin(text, context):
    secret = random.randint(1, 100)
    context['secret'] = secret
    context['moves'] = 0
    return True


def handle_guessing(text, context):
    match = re.match(regular_number, text)
    if match:
        if abs(int(text) - int(context['secret'])) <= 5:
            context['moves'] += 1
            return True
        elif int(text) > int(context['secret']):
            context['massage'] = 'Ох, увы твое число больше чем нужно!'
            context['moves'] += 1
            return False
        elif int(text) < int(context['secret']):
            context['massage'] = 'Ох, увы твое число меньше чем нужно!'
            context['moves'] += 1
            return False
    else:
        context['massage'] = 'Ну нет ты смухлевал, надо ввести именно число от 1 до 99'
        return False
