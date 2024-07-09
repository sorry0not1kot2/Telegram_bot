# 
#
#
# файл mmain.py
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import g4f
import os
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levellevel)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла секрета репозитория
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle_text_request(query):
    logger.info(f"Handling text request: {query}")
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            provider=g4f.Provider.You,
            messages=[{"role": "user", "content": query}]
        )
        result = response['choices'][0]['message']['content']
        logger.info(f"Text request result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error handling text request: {e}")
        return f"Произошла ошибка: {e}"

async def start(update: Update, context: CallbackContext) -> None:
    logger.info("Received /start command")
    await update.message.reply_text('Привет! Я бот, который работает на LLM GPT-4.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    response = await handle_text_request(user_message)
    await update.message.reply_text(response)
    logger.info(f"Received message: {user_message}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Starting bot")
    application.run_polling()

if __name__ == '__main__':
    main()

"""
# Список провайдеров и моделей
provider_models = {
    "You": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    "Forefront": ["claude-v1", "claude-v1.3"],
    "DeepAI": ["deepai-gpt", "deepai-gpt-4"]
}
"""

# конец

