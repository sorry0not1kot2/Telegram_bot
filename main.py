import asyncio
import logging
import os
import g4f
from telebot.async_telebot import AsyncTeleBot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Используем переменную окружения для токена
bot = AsyncTeleBot(BOT_TOKEN)

async def get_gpt_response(query):
    try:
        response = await g4f.ChatCompletion.create_async(
            model="gpt-4",
            messages=[{"role": "user", "content": query}],
        )
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Произошла ошибка при обращении к GPT: {str(e)}"

@
