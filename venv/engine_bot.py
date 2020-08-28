import random
import requests
import vk_api
from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import intents
import secret_settings
import handllers
import logging
from data_base import UserState
import moment_replay_handlers
from scenario import SCENARIO

log = logging.getLogger('main_log')


def logging_setup():
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('bots_warning.log', 'w')
    log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt='%d-%m-%Y %H:%M:%S')
    screen_fromatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S')
    stream_handler.setFormatter(screen_fromatter)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.WARNING)
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    log.setLevel(logging.INFO)


# Создание класса бота
class BotAlik:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    # Функция запуска бота
    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event=event)
            except Exception:
                log.exception('При работе возникла ошибка')

    # Обработчик входящих событий
    @db_session
    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info("Полученно сообщение: %s", event.object.text)
            user_id = event.object.peer_id
            state = UserState.get(user_id=str(user_id))

            if state is not None:
                self.continue_scenario(user_id=user_id, text=str(event.object.text).lower(), state=state)
            else:
                for intent in intents.INTENTS:
                    if any(token in event.object.text.lower() for token in intent['token']):
                        if intent['moment_replay']:
                            reply = getattr(moment_replay_handlers, intent['moment_replay'])
                            self.send_moment_replay(user_id=user_id, message=reply(user_id))
                        elif intent['answer']:
                            self.mail_func(user_id=user_id, send_text=intent['answer'])
                        else:
                            self.start_scenario(user_id, scenario_name=intent['scenario'], text=event.object.text)
                        break
                else:
                    self.mail_func(user_id=user_id, send_text=intents.DEFAULT_ANSWER)

        elif event.type == VkBotEventType.MESSAGE_REPLY:
            log.info("Отправленно сообщение: %s", event.object.text)
        else:
            log.warning('Получена неизвестная команда типа %s', event.type)
            return

    # Функция отправки сообщения
    def mail_func(self, send_text, user_id):
        self.api.messages.send(message=send_text,
                               random_id=random.randint(0, 2 ** 20),
                               peer_id=user_id, )

    # Функция отправки картинки
    def send_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_date = requests.post(url=upload_url, files={'photo': ('image.jpg', image, 'image/jpg')}).json()
        image_date = self.api.photos.saveMessagesPhoto(**upload_date)
        owner_id = image_date[0]['owner_id']
        media_id = image_date[0]['id']
        attachment_id = f'photo{owner_id}_{media_id}'
        self.api.messages.send(attachment=attachment_id,
                               random_id=random.randint(0, 2 ** 20),
                               peer_id=user_id, )

    # Обработчики отправки ответа бота
    def send_step(self, step, user_id, text, context):
        if 'text' in step:
            self.mail_func(send_text=step['text'].format(**context), user_id=user_id)
        if 'image' in step:
            handler = getattr(handllers, step['image'])
            image = handler(text, context)
            self.send_image(image, user_id)

    def send_moment_replay(self, user_id, message):
        if isinstance(message, str):
            self.mail_func(message, user_id)
        else:
            self.send_image(message, user_id)

    # Обработчики сценариев ивентов бота
    def start_scenario(self, user_id, scenario_name, text):
        scenario = SCENARIO[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        self.send_step(step, user_id, text, context={})
        UserState(user_id=str(user_id), scenario_name=scenario_name, current_step=first_step, context={})

    def continue_scenario(self, user_id, text, state):
        step = SCENARIO[state.scenario_name]['steps'][state.current_step]
        handler = getattr(handllers, step['handler'])
        if handler(text=text, context=state.context):
            next_step = SCENARIO[state.scenario_name]['steps'][step['next_step']]
            self.send_step(next_step, user_id, text, state.context)
            if next_step['next_step']:
                state.current_step = step['next_step']
            else:
                state.delete()
        else:
            self.mail_func(user_id=user_id, send_text=step['failure_text'].format(**state.context))


# Запуск бота
if __name__ == '__main__':
    logging_setup()
    bot = BotAlik(group_id=secret_settings.GROUP_ID, token=secret_settings.TOKEN)
    bot.run()
