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

# Хранение данных по разговорам
conversation_data = {}

async def get_gpt_response(query):
    try:
        response = await g4f.ChatCompletion.create_async(
            model="claude-3-sonnet",
            messages=[{"role": "user", "content": query}],
        )
        return response
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

@bot.message_handler(commands=['start'])
async def handle_start_command(message):
    await bot.send_message(message.chat.id, f"Привет! Я - GPT-бот. Обращайтесь по @{bot_username} или отвечайте на мои сообщения, чтобы получить ответ.")

@bot.message_handler(commands=['clear'])
async def handle_clear_command(message):
    conversation_data.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "Данные очищены.")

@bot.message_handler(func=lambda message: bot_username in message.text or (message.reply_to_message and message.reply_to_message.from_user.username == bot_username))
async def handle_message(message):
    query = message.text.replace(f"@{bot_username}", "").strip()
    
    if query:
        logger.info(f"Получен запрос: {query}")
        await bot.send_message(message.chat.id, "Обрабатываю ваш запрос...")
        
        response = await get_gpt_response(query)
        
        await bot.reply_to(message, response)
        logger.info("Ответ отправлен")
    else:
        await bot.reply_to(message, "Введите сообщение.")

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
