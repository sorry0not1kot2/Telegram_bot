import logging
import os
import nest_asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import g4f
from g4f.Provider import RetryProvider, OpenaiChat, Bard, Bing, HuggingChat, OpenAssistant

# Применение nest_asyncio
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG  # Уровень DEBUG для более подробных логов
)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я бот, использующий GPT-4. Напиши мне что-нибудь!')

# Функция для обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logging.info(f"Received message: {user_message}")
    try:
        # Использование RetryProvider для управления провайдерами
        provider = RetryProvider([OpenaiChat, Bard, Bing, HuggingChat, OpenAssistant])
        logging.info(f"Using provider: {provider}")

        response = g4f.ChatCompletion.create(
            model='gpt-3.5-turbo',  # или другая модель, если необходимо
            messages=[{"role": "user", "content": user_message}],
            provider=provider  # Указываем выбранного провайдера
        )
        logging.info(f"Raw response type: {type(response)}")
        logging.info(f"Raw response: {response}")  # Логирование для проверки структуры ответа
        
        if isinstance(response, dict):
            logging.info(f"Response keys: {response.keys()}")
            if 'choices' in response and isinstance(response['choices'], list) and len(response['choices']) > 0:
                choice = response['choices'][0]
                if 'message' in choice and isinstance(choice['message'], dict) and 'content' in choice['message']:
                    reply_text = choice['message']['content']
                elif 'text' in choice:
                    reply_text = choice['text']
                else:
                    raise ValueError("Unexpected response structure")
            else:
                raise ValueError("Unexpected response structure")
        else:
            raise TypeError("Response is not a dictionary")
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
