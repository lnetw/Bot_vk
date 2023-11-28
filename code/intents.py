# Обработчики приходящих сообщений бота
INTENTS = [
    {
        'name': 'greetings',
        'token': ('привет', 'хай', 'ку', 'здарова', 'хаюшки', 'хаюшки', 'здрасьте'),
        'scenario': None,
        'moment_replay': 'moment_greeting',
        'answer': None
    },
    {
        'name': 'abilities',
        'token': ('делаешь', 'можешь', 'способен', 'могу', 'что'),
        'scenario': None,
        'moment_replay': None,
        'answer': f'На данный момент я могу: '
                  f'\n1. Здороваться просто скажи привет'
                  f'\n2. Выдавать рандомное число просто проси или команда /roll '
                  f'\n3. Дать прогноз погоды на день просто пороси или команда /погода'
                  f'\n4. Прислать картинку котика просто попроси или команда /кот'
                  f'\n5. Могу сыграть с тобой в игру попроси или команда /игра'
    },
    {
        'name': 'name_user',
        'token': ('имя', 'зовут', 'способен'),
        'scenario': 'naming',
        'moment_replay': None,
        'answer': None
    },
    {
        'name': 'random_number',
        'token': ('случайное', 'рандомное', '/roll', 'число'),
        'scenario': None,
        'moment_replay': 'moment_random',
        'answer': None
    },
    {
        'name': 'weather',
        'token': ('погода', 'погодное', 'прогноз'),
        'scenario': 'weather forecast',
        'moment_replay': None,
        'answer': None
    },
    {
        'name': 'game',
        'token': ('игра', 'сыграем', 'поиграем', "играть"),
        'scenario': 'gaming',
        'moment_replay': None,
        'answer': None
    },
    {
        'name': 'generate_cats',
        'token': ('кота', 'котов', 'котиков', 'кошечку', 'кот'),
        'scenario': None,
        'moment_replay': 'moment_cats',
        'answer': None
    },
]
# Ответ бота на неподдерживаемые сообщения
DEFAULT_ANSWER = 'Прости я ничего не понял, можешь спросить меня что я могу!'
