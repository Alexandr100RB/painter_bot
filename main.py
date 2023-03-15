import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import telegram_token, openai_api_key

token = telegram_token
openai.api_key = openai_api_key

bot = Bot(token)
dp = Dispatcher(bot)

async def start_bot(_):
    print('Бот запущен')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Привет! Скажи, что мне что-нибудь и я это нарисую. Русский язык понимаю очеь плохо, так что"
                           " лучше пиши на английском. Генерация картинки занимает чуть больше 10 секунд.")


@dp.message_handler()
async def send(message: types.Message):
    prompt = message.text
    try:
        response = openai.Image.create(
            prompt=prompt,
            model="image-alpha-001",
            size="1024x1024",
            response_format="url"
        )

        image_url = response["data"][0]["url"]

        await bot.send_photo(chat_id=message.chat.id, photo=image_url)
    except Exception:
        await bot.send_message(message.from_user.id, "нуу, такое не осилю, давай что-то другое")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot)