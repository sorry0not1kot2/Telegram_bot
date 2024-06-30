import logging
import os
import nest_asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import g4f

# Применение nest_asyncio
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот, использующий GPT-4. Напиши мне что-нибудь!')

# Функция для обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    try:
        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',  # или другая модель, если необходимо
            messages=[{"role": "user", "content": user_message}]
        )
        logging.info(f"Response: {response}")  # Логирование для проверки структуры ответа
        reply_text = response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Ошибка при генерации ответа: {e}")
        reply_text = "Извините, произошла ошибка при обработке вашего сообщения."
    await update.message.reply_text(reply_text)

# Основная функция для запуска бота
def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    bot = Bot(token)
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
