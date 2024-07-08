# 
#
#
# файл mmain.py

# Код с провайдерами и моделями бесплатно с g4f. 
# без библиотеки siogram Файл main.py:
# Исправленная версия, работает с асинхронными функциями и телебот без аиограм

import os
from g4f import Provider
from g4f.Provider import bing
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Загрузка переменных окружения из файла секрета репозитория
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(BOT_TOKEN)

async def handle_text_request(query):
    # Используем метод для обработки текстовых запросов
    response = bing.ChatCompletion.create(prompt=query)
    return response['choices'][0]['text']

async def generate_image(prompt):
    # Используем метод для генерации изображений
    image_url = bing.ImageGeneration.create(prompt=prompt)
    return image_url['data'][0]['url']

async def analyze_photo(photo_path, description):
    # Используем метод для анализа изображений
    analysis = bing.ImageAnalysis.create(image_path=photo_path, description=description)
    return analysis['result']

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот, который может отвечать на текстовые запросы, генерировать изображения и анализировать фото. Отправьте текст или изображение с описанием.')

async def handle_message(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    if "нарисуй" in query.lower():
        image_url = await generate_image(query)
        await update.message.reply_text(f'Вот ваше изображение: {image_url}')
    else:
        response = await handle_text_request(query)
        await update.message.reply_text(response)

async def handle_photo(update: Update, context: CallbackContext) -> None:
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

