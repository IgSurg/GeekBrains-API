# e5e4cd692a72b0b66ea0a6b80255d1c3
import requests
from pprint import pprint

# api.openweathermap.org/data/2.5/weather ?  q={city name}  &    appid={API key}
city = 'Rio'
city = 'Moscow'

appid = 'e5e4cd692a72b0b66ea0a6b80255d1c3'

main_link = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'

url_params = {
    'q': city,
    'appid': appid
}

response = requests.get('https://api.openweathermap.org/data/2.5/weather',params = url_params)

if response.ok:
    j_data = response.json()
    # pprint(j_data)
    print(f"В городе {j_data['name']} температура {j_data['main']['temp'] - 273.15} градусов")
    print("В городе ",j_data['name']," температура ",j_data['main']['temp'] - 273.15," градусов")
    print(j_data)

main_link = 'https://www.lenta.ru'
response = requests.get(main_link)
print(response)
if response.ok:
    j_data = response.json()
    print(j_data)
    print()