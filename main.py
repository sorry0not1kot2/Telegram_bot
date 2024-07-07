# 
#
#
# файл mmain.py


import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
import g4f
import json

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

        # Преобразуем ответ в форматированный JSON
        response_json = json.dumps(response, indent=4)

        # Выводим структуру ответа в GitHub Actions
        github_output("gpt_response", response_json)

        # Выводим сообщение GPT в лог (асинхронно)
        if isinstance(response, dict) and 'choices' in response and len(response['choices']) > 0:
            response_text = response['choices'][0]['message']['content']
            asyncio.create_task(log_gpt_message(response_text))

        return response
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

# Функция для асинхронного вывода сообщения GPT в лог
async def log_gpt_message(response_text):
    logger.info(f"Сообщение GPT: {response_text}")
    print(f"::notice::Сообщение GPT: {response_text}")

# Функция обработки команды /start
async def start(message):
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки сообщений 
async def message_handler(message):
    text = message.text
    logger.info(f"Получено сообщение от пользователя: {text}")
    print(f"::notice::Получено сообщение от пользователя: {text}")

    response = await get_gpt_response(text)
    
    # Проверка структуры ответа
    if isinstance(response, dict) and 'choices' in response and len(response['choices']) > 0:
        response_text = response['choices'][0]['message']['content']
    else:
        response_text = response

    logger.info(f"Ответ GPT: {response_text}")
    print(f"::notice::Ответ GPT: {response_text}")

    await bot.send_message(chat_id=message.chat.id, text=response_text, parse_mode='Markdown')

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.run(bot.polling())


# конец

