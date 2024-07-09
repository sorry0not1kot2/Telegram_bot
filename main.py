# 
#
#
# файл mmain.py

import g4f
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def list_available_providers():
    try:
        # Получение списка доступных провайдеров
        available_providers = [provider for provider in dir(g4f.Provider) if not provider.startswith("__")]
        logger.info(f"Доступные провайдеры: {available_providers}")

    except Exception as e:
        logger.error(f"Error listing providers: {e}")

if __name__ == '__main__':
    list_available_providers()








"""
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import g4f
import os
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла секрета репозитория
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def handle_text_request(query):
    logger.info(f"Handling text request: {query}")
    try:
        response = g4f.ChatCompletion.create(
            model="claude",
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
    await update.message.reply_text('Привет! Я бот, который работает на LLM Claude.')

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

"""
# Bing но требует капчу или прокси
import os
import logging
from g4f import Provider
from g4f.Provider import Bing
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Загрузка переменных окружения из файла секрета репозитория
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(BOT_TOKEN)

async def handle_text_request(query):
    logger.info(f"Handling text request: {query}")
    try:
        response = Bing.create_completion(model="gpt-4", messages=[{"role": "user", "content": query}])
        result = ""
        for message in response:
            result += message['choices'][0]['message']['content']
        logger.info(f"Text request result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error handling text request: {e}")
        return f"Произошла ошибка: {e}"

async def generate_image(prompt):
    logger.info(f"Generating image for prompt: {prompt}")
    if hasattr(Bing, 'create_image'):
        try:
            response = Bing.create_image(prompt=prompt)
            result = ""
            for image in response:
                result += image['data'][0]['url']
            logger.info(f"Generated image URL: {result}")
            return result
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return f"Произошла ошибка: {e}"
    else:
        logger.warning("Method create_image not supported.")
        return "Метод create_image не поддерживается."

async def analyze_photo(photo_path, description):
    logger.info(f"Analyzing photo: {photo_path} with description: {description}")
    try:
        response = Bing.analyze_image(image_path=photo_path, description=description)
        result = ""
        for analysis in response:
            result += analysis['result']
        logger.info(f"Photo analysis result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error analyzing photo: {e}")
        return f"Произошла ошибка: {e}"

async def start(update: Update, context: CallbackContext) -> None:
    logger.info("Received /start command")
    await update.message.reply_text('Привет! Я бот, который может отвечать на текстовые запросы, генерировать изображения и анализировать фото. Отправьте текст или изображение с описанием.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    logger.info(f"Received message: {query}")
    if "нарисуй" in query.lower():
        image_url = await generate_image(query)
        await update.message.reply_text(f'Вот ваше изображение: {image_url}')
    else:
        response = await handle_text_request(query)
        await update.message.reply_text(response)

async def handle_photo(update: Update, context: CallbackContext) -> None:
    logger.info("Received photo")
    photo_file = await update.message.photo[-1].get_file()
    photo_path = await photo_file.download()
    description = update.message.caption if update.message.caption else "анализировать"
    analysis = await analyze_photo(photo_path, description)
    await update.message.reply_text(analysis)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    logger.info("Starting bot")
    application.run_polling()

if __name__ == '__main__':
    main()
"""
"""
# Список провайдеров и моделей
provider_models = {
    "You": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    "Forefront": ["claude-v1", "claude-v1.3"],
    "DeepAI": ["deepai-gpt", "deepai-gpt-4"]
}
"""

# конец

