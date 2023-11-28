# Часть отвечающая за обработки сценариев бота
SCENARIO = {
    'naming': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите пожалуйста имя, что бы я мог к вам обращаться:',
                'failure_text': 'Имя может состоять только из букв русского или латинского алфавита, поробуйте еще раз!',
                'handler': 'handle_name',
                'next_step': 'step2',
            },
            'step2': {
                'text': 'Введите пожалуйста свое отчество:',
                'failure_text': 'Фамилия может состоять только из букв русского или латинского алфавита, '
                                'поробуйте еще раз!',
                'handler': 'handle_surname',
                'next_step': 'step3',
            },
            'step3': {
                'text': 'Приятно познакомиться {name} {surname} лови котика!',
                'image': 'handler_generate_image',
                'failure_text': None,
                'handler': None,
                'next_step': None,
            }
        }
    },
    'weather forecast': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Введите город в котором хотите посмотреть прогноз погоды:',
                'failure_text': 'Следует ввести только название города!',
                'handler': 'handle_city',
                'next_step': 'step2',
            },
            'step2': {
                'text': 'Введите день когда вы хотите получить прогноз в формате DD-MM-YYYY на ближайший месяц,'
                        ' либо вчера, сегодня, завтра',
                'failure_text': 'Дата может быть только в формате DD-MM-YYYY на ближайший месяц,'
                                ' либо вчера, сегодня, завтра',
                'handler': 'handle_weather',
                'next_step': 'step3',
            },
            'step3': {
                'text': 'В {city} {date} {condition} температура {temperature}!',
                'failure_text': None,
                'handler': None,
                'next_step': None,
            }
        }
    },
    'gaming': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Я загадал число от 1 до 99 попробуй его угадать с точностью до 5,'
                        'каждый раз я буду говорить в какую сторону ты ошибся больше или меньше, все понял?',
                'failure_text': 'Он не нужен',
                'handler': 'handle_game_begin',
                'next_step': 'step2',
            },
            'step2': {
                'text': 'Хорошо тогда угадай число!',
                'failure_text': "{massage}!",
                'handler': 'handle_guessing',
                'next_step': 'step3',
            },
            'step3': {
                'text': 'О поздравляю ты победил меня, я загадал {secret}, ты выйграл за {moves} ходов!',
                'failure_text': None,
                'handler': None,
                'next_step': None,
            }
        }
    },
}
