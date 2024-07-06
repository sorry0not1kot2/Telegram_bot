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

# Список провайдеров
providers = [g4f.Provider.You]

# Функция для получения ответа от провайдера
async def get_response(text):
    for provider in providers:
        try:
            response = g4f.ChatCompletion.create(
                model="claude-3-sonnet",
                provider=provider,
                messages=[{"role": "user", "content": text}],
                max_tokens=1024,
                no_sandbox=True  # Добавляем параметр no_sandbox
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Ошибка при использовании провайдера {provider}: {e}")
    return "Извините, все провайдеры недоступны в данный момент."

# Функция обработки команды /start
async def start(message):
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки сообщений 
async def message_handler(message):
    text = message.text
    response_text = await get_response(text)
    await bot.send_message(chat_id=message.chat.id, text=response_text)

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.get_event_loop().run_until_complete(bot.polling())

