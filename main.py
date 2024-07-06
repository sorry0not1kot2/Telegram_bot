# 
#
#
# файл mmain.py

import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f.Provider import You

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Настройка провайдера
provider = You()

# Функция обработки команды /start
async def start(message):
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки сообщений 
async def message_handler(message):
    text = message.text
    
    # Генерация ответа с помощью модели claude-3-sonnet
    response = provider.Completion.create(
        model="claude-3-sonnet",
        prompt=text,
        max_tokens=1024
    )
    
    # Отправка ответа в чат
    await bot.send_message(chat_id=message.chat.id, text=response['choices'][0]['text'])

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.get_event_loop().run_until_complete(bot.polling())
