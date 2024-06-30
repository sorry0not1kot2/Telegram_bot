import logging
import os
import nest_asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Применение nest_asyncio
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Уровень DEBUG для более подробных логов
)

# Установка токена Hugging Face
openai.api_key = os.getenv('HUGGING_FACE_TOKEN')  # Убедитесь, что токен установлен в переменных окружения
openai.api_base = "http://localhost:1337/v1"  # Установка базового URL для локального сервера

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот, использующий GPT-4. Напиши мне что-нибудь!')

# Функция для обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logging.info(f"Received message: {user_message}")
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',  # или другая модель, если необходимо
            messages=[{"role": "user", "content": user_message}],
            stream=True
        )
        
        reply_text = ""
        if isinstance(response, dict):
            reply_text = response['choices'][0]['message']['content']
        else:
            for token in response:
                content = token["choices"][0]["delta"].get("content")
                if content is not None:
                    reply_text += content

        logging.info(f"Reply text: {reply_text}")
    except Exception as e:
        logging.error(f"Ошибка при генерации ответа: {e}", exc_info=True)  # Добавлено exc_info=True для полного трейсбека
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
