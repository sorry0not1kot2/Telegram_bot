# файл бота main.py

import os
import asyncio
import logging
import json
from telebot.async_telebot import AsyncTeleBot
import g4f

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Словарь для хранения истории чата
chat_history = {}

# Словарь для хранения временных сообщений
temp_messages = {}

# Функция для разбиения длинного сообщения на части
def split_message(message, max_length=4090):
    parts = []
    while len(message) > max_length:
        split_index = max_length
        while split_index > 0 and message[split_index] not in [' ', '\n', '.']:
            split_index -= 1
        if split_index == 0:
            split_index = max_length
        parts.append(message[:split_index].rstrip())
        message = message[split_index:].lstrip()
    parts.append(message)
    return parts

# Асинхронная функция для получения ответа от GPT
async def get_gpt_response(user_id, user_message):
    try:
        # Добавление сообщения пользователя в историю чата
        chat_history.setdefault(user_id, []).append({"role": "user", "content": user_message})
        logging.info("Отправка запроса к g4f")
        
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=chat_history[user_id],
            no_sandbox=True
        )
        
        logging.info(f"Получен ответ от g4f: {response}")
        
        # Проверка на пустой ответ
        if not response:
            logging.warning("Получен пустой ответ от g4f")
            return "Извините, я не смог сгенерировать ответ. Попробуйте еще раз."
        
        if isinstance(response, str):
            try:
                response_data = json.loads(response)
                bot_response = response_data['choices'][0]['message']['content']
            except json.JSONDecodeError:
                bot_response = response  # Используем ответ как есть, если это не JSON
        elif isinstance(response, dict):
            bot_response = response.get('choices', [{}])[0].get('message', {}).get('content', 'Нет ответа')
        else:
            raise ValueError("Неожиданный формат ответа от API")
        
        # Добавление ответа бота в историю чата
        chat_history[user_id].append({"role": "assistant", "content": bot_response})
        return bot_response
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        return "Произошла ошибка при обработке вашего сообщения."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM GPT-4o.')

# Обработчик команды /clear
@bot.message_handler(commands=['clear'])
async def clear(message):
    chat_history.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "История чата очищена.")

# Асинхронная функция для обработки сообщений
@bot.message_handler(content_types=['text'])
async def handle_message(message):
    user_id = message.chat.id
    user_message = message.text
    logging.info(f"Получено сообщение: {user_message}")
    
    # Инициализация истории чата для нового пользователя
    chat_history.setdefault(user_id, [])
    
    # Сохранение временного сообщения
    if user_id in temp_messages:
        temp_messages[user_id] += " " + user_message
    else:
        temp_messages[user_id] = user_message
    
    # Задержка перед отправкой сообщения к LLM
    await asyncio.sleep(0.1)
    
    # Проверка, пришло ли новое сообщение от того же пользователя
    while True:
        await asyncio.sleep(0.05)
        if temp_messages[user_id] != user_message:
            user_message = temp_messages.pop(user_id)
            break
        elif len(temp_messages[user_id].split()) > 1:
            break
    
    # Отправка сообщения "Думаю..." один раз
    if user_id not in temp_messages:
        thinking_message = await bot.send_message(user_id, "Думаю...")
        temp_messages[user_id] = {"thinking_message": thinking_message, "user_message": user_message}
    else:
        temp_messages[user_id]["user_message"] += " " + user_message

    # Получение ответа от GPT
    bot_response = await get_gpt_response(user_id, temp_messages[user_id]["user_message"])
    
    # Удаление сообщения "Думаю..."
    await bot.delete_message(chat_id=user_id, message_id=temp_messages[user_id]["thinking_message"].message_id)
    temp_messages.pop(user_id)
    
    # Разбиение длинного ответа на части и отправка их по частям
    for part in split_message(bot_response):
        await bot.send_message(user_id, part)

# Асинхронная функция main для запуска бота
async def main():
    while True:
        try:
            logging.info("Бот запущен")
            await bot.polling(non_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в основном цикле бота: {e}")
            await asyncio.sleep(5)  # Пауза перед повторной попыткой

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())



"""
import os
import asyncio
import logging
import json
from telebot.async_telebot import AsyncTeleBot
import g4f

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Словарь для хранения истории чата
chat_history = {}

# Функция для разбиения длинного сообщения на части
def split_message(message, max_length=4090):
    parts = []
    while len(message) > max_length:
        split_index = max_length
        while split_index > 0 and message[split_index] not in [' ', '\n', '.']:
            split_index -= 1
        if split_index == 0:
            split_index = max_length
        parts.append(message[:split_index].rstrip())
        message = message[split_index:].lstrip()
    parts.append(message)
    return parts

# Асинхронная функция для получения ответа от GPT
async def get_gpt_response(user_id, user_message):
    try:
        # Добавление сообщения пользователя в историю чата
        chat_history.setdefault(user_id, []).append({"role": "user", "content": user_message})
        logging.info("Отправка запроса к g4f")
        
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=chat_history[user_id],
            no_sandbox=True
        )
        
        logging.info(f"Получен ответ от g4f: {response}")
        
        # Проверка на пустой ответ
        if not response:
            logging.warning("Получен пустой ответ от g4f")
            return "Извините, я не смог сгенерировать ответ. Попробуйте еще раз."
        
        if isinstance(response, str):
            try:
                response_data = json.loads(response)
                bot_response = response_data['choices'][0]['message']['content']
            except json.JSONDecodeError:
                bot_response = response  # Используем ответ как есть, если это не JSON
        elif isinstance(response, dict):
            bot_response = response.get('choices', [{}])[0].get('message', {}).get('content', 'Нет ответа')
        else:
            raise ValueError("Неожиданный формат ответа от API")
        
        # Добавление ответа бота в историю чата
        chat_history[user_id].append({"role": "assistant", "content": bot_response})
        return bot_response
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        return "Произошла ошибка при обработке вашего сообщения."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM GPT-4o.')

# Обработчик команды /clear
@bot.message_handler(commands=['clear'])
async def clear(message):
    chat_history.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "История чата очищена.")

# Асинхронная функция для обработки сообщений
@bot.message_handler(content_types=['text'])
async def handle_message(message):
    user_id = message.chat.id
    user_message = message.text
    logging.info(f"Получено сообщение: {user_message}")
    
    # Инициализация истории чата для нового пользователя
    chat_history.setdefault(user_id, [])
    
    # Отправка сообщения "Думаю..."
    thinking_message = await bot.send_message(user_id, "Думаю...")
    bot_response = await get_gpt_response(user_id, user_message)
    
    # Удаление сообщения "Думаю..."
    await bot.delete_message(chat_id=user_id, message_id=thinking_message.message_id)
    
    # Разбиение длинного ответа на части и отправка их по частям
    for part in split_message(bot_response):
        await bot.send_message(user_id, part)

# Асинхронная функция main для запуска бота
async def main():
    while True:
        try:
            logging.info("Бот запущен")
            await bot.polling(non_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в основном цикле бота: {e}")
            await asyncio.sleep(5)  # Пауза перед повторной попыткой

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
"""


"""
import os
import asyncio
import logging
import json
from telebot.async_telebot import AsyncTeleBot
import g4f

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Словарь для хранения истории чата
chat_history = {}

# Функция для разбиения длинного сообщения на части
def split_message(message, max_length=4090):
    parts = []
    while len(message) > max_length:
        split_index = max_length
        while split_index > 0 and message[split_index] not in [' ', '\n', '.']:
            split_index -= 1
        if split_index == 0:
            split_index = max_length
        parts.append(message[:split_index].rstrip())
        message = message[split_index:].lstrip()
    parts.append(message)
    return parts

# Асинхронная функция для получения ответа от GPT
async def get_gpt_response(user_id, user_message):
    try:
        # Добавление сообщения пользователя в историю чата
        chat_history[user_id].append({"role": "user", "content": user_message})

        logging.info("Отправка запроса к g4f")
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=chat_history[user_id],
            no_sandbox=True
        )
        logging.info(f"Получен ответ от g4f: {response}")

        # Проверка на пустой ответ
        if not response:
            logging.warning("Получен пустой ответ от g4f")
            return "Извините, я не смог сгенерировать ответ. Попробуйте еще раз."

        if isinstance(response, str):
            try:
                response_data = json.loads(response)
                bot_response = response_data['choices'][0]['message']['content']
            except json.JSONDecodeError:
                bot_response = response  # Используем ответ как есть, если это не JSON
        elif isinstance(response, dict):
            bot_response = response.get('choices', [{}])[0].get('message', {}).get('content', 'Нет ответа')
        else:
            raise ValueError("Неожиданный формат ответа от API")

        # Добавление ответа бота в историю чата
        chat_history[user_id].append({"role": "assistant", "content": bot_response})
        return bot_response
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        return "Произошла ошибка при обработке вашего сообщения."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM GPT-4o.')

# Обработчик команды /clear
@bot.message_handler(commands=['clear'])
async def clear(message):
    chat_history.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "История чата очищена.")

# Асинхронная функция для обработки сообщений
@bot.message_handler(content_types=['text'])
async def handle_message(message):
    user_id = message.chat.id
    user_message = message.text
    logging.info(f"Получено сообщение: {user_message}")

    # Инициализация истории чата для нового пользователя
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Отправка сообщения "Думаю..."
    thinking_message = await bot.send_message(user_id, "Думаю...")

    bot_response = await get_gpt_response(user_id, user_message)

    # Удаление сообщения "Думаю..."
    await bot.delete_message(chat_id=user_id, message_id=thinking_message.message_id)

    # Разбиение длинного ответа на части и отправка их по частям
    for part in split_message(bot_response):
        await bot.send_message(user_id, part)

# Асинхронная функция main для запуска бота
async def main():
    while True:
        try:
            logging.info("Бот запущен")
            await bot.polling(non_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в основном цикле бота: {e}")
            await asyncio.sleep(5)  # Пауза перед повторной попыткой

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
"""


"""
import os
import asyncio
import logging
import json
from telebot.async_telebot import AsyncTeleBot
import g4f

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Словарь для хранения истории чата
chat_history = {}

# Функция для разбиения длинного сообщения на части
def split_message(message, max_length=4090):
    parts = []
    while len(message) > max_length:
        split_index = max_length
        while split_index > 0 and message[split_index] not in [' ', '\n', '.']:
            split_index -= 1
        if split_index == 0:
            split_index = max_length
        parts.append(message[:split_index].rstrip())
        message = message[split_index:].lstrip()
    parts.append(message)
    return parts

# Асинхронная функция для получения ответа от GPT
async def get_gpt_response(user_id, user_message):
    try:
        # Добавление сообщения пользователя в историю чата
        chat_history[user_id].append({"role": "user", "content": user_message})

        logging.info("Отправка запроса к g4f")
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4o",
            messages=chat_history[user_id],
            no_sandbox=True
        )
        logging.info(f"Получен ответ от g4f: {response}")

        # Проверка на пустой ответ
        if not response:
            logging.warning("Получен пустой ответ от g4f")
            return "Извините, я не смог сгенерировать ответ. Попробуйте еще раз."

        if isinstance(response, str):
            try:
                response_data = json.loads(response)
                bot_response = response_data['choices'][0]['message']['content']
            except json.JSONDecodeError:
                bot_response = response  # Используем ответ как есть, если это не JSON
        elif isinstance(response, dict):
            bot_response = response.get('choices', [{}])[0].get('message', {}).get('content', 'Нет ответа')
        else:
            raise ValueError("Неожиданный формат ответа от API")

        # Добавление ответа бота в историю чата
        chat_history[user_id].append({"role": "assistant", "content": bot_response})
        return bot_response
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        return "Произошла ошибка при обработке вашего сообщения."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM GPT-4o.')

# Обработчик команды /clear
@bot.message_handler(commands=['clear'])
async def clear(message):
    chat_history.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "История чата очищена.")

# Асинхронная функция для обработки сообщений
@bot.message_handler(content_types=['text'])
async def handle_message(message):
    user_id = message.chat.id
    user_message = message.text
    logging.info(f"Получено сообщение: {user_message}")

    # Инициализация истории чата для нового пользователя
    if user_id not in chat_history:
        chat_history[user_id] = []

    bot_response = await get_gpt_response(user_id, user_message)

    # Разбиение длинного ответа на части и отправка их по частям
    for part in split_message(bot_response):
        await bot.send_message(message.chat.id, part)

# Асинхронная функция main для запуска бота
async def main():
    while True:
        try:
            logging.info("Бот запущен")
            await bot.polling(non_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в основном цикле бота: {e}")
            await asyncio.sleep(5)  # Пауза перед повторной попыткой

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
"""
