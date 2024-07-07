# 
#
#
# файл mmain.py
"""
import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
import g4f
import aiohttp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Словарь для хранения истории сообщений
chat_histories = {}

# Функция для получения ответа от GPT-4
async def get_gpt_response(chat_id, query):
    try:
        # Получение истории сообщений для текущего чата
        history = chat_histories.get(chat_id, [])
        
        # Добавление нового сообщения в историю
        history.append({"role": "user", "content": query})
        
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=history,
        )
        
        # Выводим весь ответ для отладки
        logger.info(f"Ответ от GPT: {response}")
        
        # Сохраняем ответ в файл
        with open('response.json', 'w') as f:
            f.write(str(response))
        
        # Проверка структуры ответа
        if isinstance(response, dict) and 'choices' in response:
            choice = response['choices'][0]
            if isinstance(choice, dict) and 'message' in choice:
                message = choice['message']
                if isinstance(message, dict) and 'content' in message:
                    content = message['content']
                    history.append({"role": "assistant", "content": content})
                    chat_histories[chat_id] = history
                    return content
        
        raise ValueError("Unexpected response format")
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

# Функция обработки команды /start
async def start(message):
    await bot.send_message(chat_id=message.chat.id, text="Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки сообщений 
async def message_handler(message):
    text = message.text
    chat_id = message.chat.id
    response_text = await get_gpt_response(chat_id, text)
    await bot.send_message(chat_id=chat_id, text=response_text, parse_mode='Markdown')

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Проверка инициализации бота
async def main():
    await bot.get_me()
    if bot.user is None:
        logger.error("Не удалось получить информацию о боте. Проверьте токен.")
        return
    try:
        await bot.polling(none_stop=True, interval=1, timeout=20)
    finally:
        await bot.close_session()

# Запуск бота
asyncio.run(main())





"""
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

"""
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
    
    await bot.send_message(chat_id=message.chat.id, text=response_text)

# Добавление обработчиков команд и сообщений
bot.register_message_handler(start, commands=['start'])
bot.register_message_handler(message_handler, content_types=['text'])

# Запуск бота
asyncio.run(bot.polling())
"""
