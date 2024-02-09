from firebase import firebase
import requests
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler


def weather():
    city = "Thai Nguyen"

    # Lấy ngày hôm qua
    yesterday = datetime.now() - timedelta(days=1)

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=093bc10f5336f52a5c3c761e7b731280&units=metric'.format(
        city)
    res = requests.get(url)
    data = res.json()

    temp = data['main']['temp']
    humi = data['main']['humidity']
    wind_speed = data['wind']['speed']
    formatted_time = yesterday.strftime('%Y-%m-%d %H:%M')

    print('Temperature:', temp, 'C')
    print('Humidity:', humi, '%')
    print('Wind Speed:', wind_speed, 'm/s')

    firebase_instance = firebase.FirebaseApplication('https://w-t-tnut-default-rtdb.firebaseio.com', None)
    user = 'Bach Duy'
    data = {'temp': temp, 'humi': humi, 'wind_speed': wind_speed}
    result = firebase_instance.post(f'/{user}/Thai Nguyen/{formatted_time}', data)
    print(result)


weather()

scheduler = BlockingScheduler()
scheduler.add_job(weather, 'cron', minute='*/1')
try:
    print("Chương trình đang chờ để được cập nhật... (Nhấn Ctrl+C để dừng)")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Chương trình đã dừng.")
