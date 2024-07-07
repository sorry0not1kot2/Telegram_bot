# 
#
#
# файл mmain.py


import asyncio
imporimport asyncio
import logging
import os
import g4f
from telegram import Bot, Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
from telegram.constants import ParseMode
import nest_asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)

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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на основе GPT-4. Спроси меня о чем угодно.")

# Функция обработки команды /clear
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in context.bot_data:
        context.bot_data[user_id]["history"] = []
        await update.message.reply_text("История очищена.")

# Функция обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # Инициализируем историю для пользователя
    if user_id not in context.bot_data:
        context.bot_data[user_id] = {"history": []}

    history = context.bot_data[user_id]["history"]

    response = await get_gpt_response(text)
    
    # Проверка структуры ответа
    if isinstance(response, dict) and 'choices' in response and len(response['choices']) > 0:
        response_text = response['choices'][0]['message']['content']
    else:
        response_text = response

    history.append({"user": text, "bot": response_text})

    await update.message.reply_text(response_text, parse_mode=ParseMode.MARKDOWN)

# Функция обработки ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_error_handler(error_handler)

    logger.info("Запуск бота...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())

# конец

