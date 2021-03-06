import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def get_repo(name):
    req = requests.get(f'https://api.github.com/users/{name}/repos')
    with open('les01/repo.json', 'w') as f:
        json.dump(req.json(), f)
    print(f'Репозитории пользователя {name}')
    for i in req.json():
        print(f'{i["name"]}')


def get_weather():
    city = input('Введите название города ')
    api_key = os.getenv("API_KEY", None)
    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru')
    a = req.json()
    print(f'В городе {a["name"]} температура {a["main"]["temp"]} градусов цельсия')


get_repo('VladimirAlchin')
# test city Naberezhnye Chelny
get_weather()
