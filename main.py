
import requests
import time
from environs import Env

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

BOT_TOKEN: str = env('BOT_TOKEN_START')
API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://aws.random.cat/meow'
API_DOGS_URL: str = 'https://random.dog/woof.json'
TEXT_START: str = 'Ура! Классный апдейт!'
TEXT_ORDER: str = 'Заказывай'
ERROR_TEXT: str = 'Здесь должна была быть картинка с котиком или собачкой :('
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:

            offset = result['update_id']
            chat_id = result['message']['from']['id']
            if result['message']['text'] == '/start':
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT_START}')
            elif result['message']['text'] == '/cat':
                cat_response = requests.get(API_CATS_URL)
                if cat_response.status_code == 200:
                    cat_link = cat_response.json()['file']
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
            elif result['message']['text'] == '/dog':
                dog_response = requests.get(API_DOGS_URL)
                if dog_response.status_code == 200:
                    dog_link = dog_response.json()['url']
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={dog_link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
            elif result['message']['text'] == '/order':
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT_ORDER}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text=Следуй командам!')

    time.sleep(1)
    counter += 1
