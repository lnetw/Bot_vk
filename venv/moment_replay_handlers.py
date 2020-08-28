import random

from vk_api import vk_api

from generate_image import generate_cats
from secret_settings import TOKEN


def moment_random(user_id):
    return f'УУУУ махалай махалай ииии ваше число - {random.randint(0, 2 ** 10)}'


def moment_greeting(user_id):
    vk_ = vk_api.VkApi(token=TOKEN)
    api_ = vk_.get_api()
    name = api_.users.get(user_id=user_id)
    user_name = str(name[0]['first_name'] + ' ' + name[0]['last_name'])
    if user_name:
        return f'Здравствуйте, {user_name}!'
    else:
        return f'Здравствуйте!'

def moment_cats(user_id):
    return generate_cats()