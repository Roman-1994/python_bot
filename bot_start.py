from aiogram import Bot, Dispatcher, executor, types
import requests
from environs import Env

env = Env()  # Создаем экземпляр класса Env
env.read_env()  # Методом read_env() читаем файл .env и загружаем из него переменные в окружение

BOT_TOKEN: str = env('BOT_TOKEN_START')
API_CATS_URL: str = 'https://aws.random.cat/meow'
API_DOGS_URL: str = 'https://random.dog/woof.json'
ERROR_TEXT: str = 'Здесь должна была быть картинка с котиком или собачкой :('

# Создаем объекты бота и диспетчера
bot: Bot = Bot(token=BOT_TOKEN)
dp: Dispatcher = Dispatcher(bot)


# Этот хэндлер будет срабатывать на команду "/start"
async def process_start_command(message: types.Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
async def process_help_command(message: types.Message):
    await message.answer('Напиши мне что-нибудь и в ответ я пришлю тебе твое сообщение')


# Этот хэндлер будет срабатывать на команду "/cat"
async def process_cat_command(message: types.Message):
    cat_response = requests.get(API_CATS_URL)
    if cat_response.status_code == 200:
        cat_link = cat_response.json()['file']
        await message.answer_photo(cat_link)
    else:
        await message.answer(ERROR_TEXT)


# Этот хэндлер будет срабатывать на команду "/dog"
async def process_dog_command(message: types.Message):
    dog_response = requests.get(API_DOGS_URL)
    if dog_response.status_code == 200:
        dog_link = dog_response.json()['url']
        await message.answer_photo(dog_link)
    else:
        await message.answer(ERROR_TEXT)


# Этот хэндлер будет срабатывать на стикеры
async def send_sticker_echo(message: types.Message):
    await message.answer_sticker(message.sticker.file_id)


async def process_any_update(message: types.Message):
    # Выводим апдейт в терминал
    print(message)
    # Отправляем сообщение в чат, откуда пришел апдейт
    await message.answer('Вы что-то прислали')


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения, кроме команд "/start" и "/help"
async def send_echo(message: types.Message):
    await message.reply(message.text)


dp.register_message_handler(process_start_command, commands='start')
dp.register_message_handler(process_help_command, commands='contacts')
dp.register_message_handler(process_cat_command, commands='cat')
dp.register_message_handler(process_dog_command, commands='dog')
dp.register_message_handler(send_sticker_echo, content_types=['sticker'])
dp.register_message_handler(send_echo)
dp.register_message_handler(process_any_update, content_types=['any'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


#Другой способ регистрации хэндлеров это использование декораторов
'''
@dp.message_handler(commands=['start'])
@dp.message_handler(commands=['help'])
@dp.message_handler(commands=['cat'])
@dp.message_handler(commands=['dog'])
@dp.message_handler()
'''