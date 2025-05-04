import requests
import json
response = requests.get('https://api.openweathermap.org/data/2.5/weather?lat=51.699573&lon=39.190317&appid=60b38f9ab0abb04092db9e20c61e3f20').json()
# data = response.json()
# data = dict(response.text)
# print(type(data))
print(response)
# print(response["name"])