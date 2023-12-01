#1358a200ce2b4c8f97c170631232911

#https://api.weatherapi.com/v1/current.json?key=1358a200ce2b4c8f97c170631232911&q=59.93,30.31

#curl "https://api.weatherapi.com/v1/current.json?key=1358a200ce2b4c8f97c170631232911&q=59.93,30.31"

import requests

key = "1358a200ce2b4c8f97c170631232911"
lat = "59.93"  # широта в градусах
lon = "30.31"  # долгота в градусах

url = f"https://api.weatherapi.com/v1/current.json?key={key}&q={lat},{lon}"
response = requests.get(url)  # отправление GET запроса и получение ответа от сервера
print(response.json())  # получение JSON из ответа

# ad5af5f6-da8a-4c9c-8c6a-d6c937703b58 яндекс ключ
import requests

key = "ad5af5f6-da8a-4c9c-8c6a-d6c937703b58"
lat = "59.93"  # широта в градусах
lon = "30.31"  # долгота в градусах

url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"
headers={"X-Yandex-API-Key": f"{key}"}

response = requests.get(url, headers=headers)
print(response.json())