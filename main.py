import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import use, Provider

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Установка провайдера без API-ключей
use('claude')

# Функция обработки команды /start
async def start(message):
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки сообщений 
async def message_handler(message):
    # Получение текста сообщения
    text = message.text
    
    # Генерация ответа с помощью GPT-4
    response = use('claude').Completion.create(prompt=text, max_tokens=1024)
    
    # Отправка ответа в чат
    await bot.send_message(chat_id=message.chat.id, text=response.text)

# Настройка бота
bot = AsyncTeleBot(BOT_TOKEN)

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.get_event_loop().run_until_complete(bot.polling())
