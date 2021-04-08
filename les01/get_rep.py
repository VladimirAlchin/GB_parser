import requests
import json


def get_repo(name):
    req = requests.get(f'https://api.github.com/users/{name}/repos')
    with open('les01/repo.json', 'w') as f:
        json.dump(req.json(), f)
    print(f'Репозитории пользователя {name}')
    for i in req.json():
        print(i['name'])


def get_weather():
    city = input('Введите название города ')
    api_key = 'cc76ab0d5a9fcf0f6786364eafa6303e'
    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru')
    a = req.json()
    print(f'cite {a["id"]} \nid {a["name"]} \ntemp {a["main"]["temp"]}')


# get_repo('VladimirAlchin')
# test Naberezhnye Chelny
get_weather()
