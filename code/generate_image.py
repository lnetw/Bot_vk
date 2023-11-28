from io import BytesIO
import random
import requests
from PIL import Image, ImageDraw, ImageFont

IMAGE_PATH = 'files/image.png'
FONT_PATH = 'files/OpenSans-Regular.ttf'
BLACK = (0, 0, 0, 255)
NAME_OFFSET = (10, 10)
EMAIL_OFFSET = (10, 10)
AVATAR_SIZE = (150)
AVATAR_OFFSET = (100, 100)


# Функция создания абстрактного билета
def generate_ticket(name, email):
    base = Image.open(IMAGE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, 40)
    d = ImageDraw.Draw(base)
    d.text(NAME_OFFSET, name, font=font, fill=BLACK)
    d.text(EMAIL_OFFSET, email, font=font, fill=BLACK)
    response = requests.get(url=f'https://api.adorable.io/avatars/{AVATAR_SIZE}/{email}')
    avatar_file = BytesIO(response.content)
    avatar = Image.open(avatar_file)
    base.paste(avatar, AVATAR_OFFSET)
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)
    return temp_file


#  Функция генерации котов
def generate_cats():
    hight = random.randint(0, 1024)
    weight = random.randint(0, 1024)
    response = requests.get(url=f'https://placekitten.com/{hight}/{weight}')
    temp_file = BytesIO(response.content)
    temp_file.seek(0)
    return temp_file
