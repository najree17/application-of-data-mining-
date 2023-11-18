import requests
import json
import random
import datetime
import holidays


print('=================== Start ===================')
WEATHER_DATA: list = []
current_date: str = '28-01-2021'
NG_HOLIDAYS = holidays.country_holidays('NG')
CSV_TEXT = 'DATE(YEAR/MONTH/DAY/HOURS),ENERGY CONSUMPTION,TEMPERATURE(C),' \
    'PRESSURE,HUMIDITY,WEATHER CODE,WIND DIRECTION(DEGREE),WIND SPEED(KMPH),' \
    'WORKDAY,PUBLIC HOLIDAY\n'


def flatten_hour(date, payload):
    is_weekday = 0 if datetime.datetime.strptime(date, '%Y-%m-%d').weekday() > 4 else 1
    is_holiday = 1 if date in NG_HOLIDAYS else 0
    txt = f"{date} {payload['time'][:-2].rjust(2, '0')}:00, 0, {payload['tempC']}, " \
        f"{payload['pressure']}, {payload['humidity']}, {payload['weatherCode']}," \
        f"{payload['winddirDegree']}, {payload['windspeedKmph']}, {is_weekday}, {is_holiday}"
    global CSV_TEXT
    CSV_TEXT += f'{txt}\n'
    return txt


while True:
    if current_date == '2023-08-28':
        print('=================== Done ===================')
        break
    api_key = '02139e19e7504751bcc144017230811'
    URL: str = 'https://api.worldweatheronline.com/premium/v1/past-weather.ashx' \
        f'?key={api_key}&q=Kaduna%20North&format=json' \
        f'&date={current_date}&enddate=28-08-2023&tp=1'
    res = requests.get(URL)
    print(current_date)
    data = res.json()['data']['weather']
    day_data = [[flatten_hour(day['date'], hour) for hour in day['hourly']] for day in data[:-1]]
    WEATHER_DATA += day_data
    current_date = data[-1]['date']

with open('all.csv', "w") as outfile:
    outfile.write(CSV_TEXT)