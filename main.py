import asyncio
import logging
import os
import g4f
from telebot.async_telebot import AsyncTeleBot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Получение имени пользователя бота
bot_info = asyncio.run(bot.get_me())
bot_username = bot_info.username

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

@bot.message_handler(func=lambda message: bot_username in message.text)
async def handle_message(message):
    query = message.text
    
    if query:
        logger.info(f"Получен запрос: {query}")
        await bot.send_message(message.chat.id, "Обрабатываю ваш запрос...")
        
        response = await get_gpt_response(query)
        
        await bot.reply_to(message, response)
        logger.info("Ответ отправлен")
    else:
        await bot.reply_to(message, "Пожалуйста, введите сообщение.")

# Функция для запуска бота
async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {str(e)}")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
