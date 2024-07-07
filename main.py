# 
#
#
# файл mmain.py


import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
import g4f

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Функция для получения ответа от GPT-4
async def get_gpt_response(query):
    try:
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=[{"role": "user", "content": query}],
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

# Функция обработки команды /start
async def start(message):
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки сообщений 
async def message_handler(message):
    text = message.text
    response = await get_gpt_response(text)
    await bot.send_message(chat_id=message.chat.id, text=response)

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Асинхронная функция main для запуска бота
async def main():
    await bot.polling()

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())


# конец

