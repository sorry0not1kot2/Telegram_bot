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

# Функция для вывода информации в GitHub Actions
def github_output(key, value):
    print(f'::set-output name={key}::{value}')

# Функция для получения ответа от GPT-4
async def get_gpt_response(query):
    try:
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=[{"role": "user", "content": query}],
        )
        
        # Вывод структуры ответа в GitHub Actions
        github_output("gpt_response", response)
        
        return response
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
    
    # Проверка структуры ответа
    if isinstance(response, dict) and 'choices' in response and len(response['choices']) > 0:
        response_text = response['choices'][0]['message']['content']
    else:
        response_text = response
    
    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode='Markdown')

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.run(bot.polling())


"""
# работающая версия с парсингом маркдаун
# без условий чата и без отсылки ботом сообщения я подумаю
# работает от провайдера You с gpt-4o  х.з. как
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
        return response
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
    
    # Проверка структуры ответа
    if isinstance(response, dict) and 'choices' in response and len(response['choices']) > 0:
        response_text = response['choices'][0]['message']['content']
    else:
        response_text = response
    
    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode='Markdown')

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.run(bot.polling())


# конец

"""
