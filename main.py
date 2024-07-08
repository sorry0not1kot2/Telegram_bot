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
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Загрузка переменных окружения из файла секрета репозитория
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(BOT_TOKEN)

def handle_text_request(query):
    response = bing.process(query)
    return response

def generate_image(prompt):
    image_url = bing.generate_image(prompt)
    return image_url

def analyze_photo(photo_path, description):
    analysis = bing.analyze_image(photo_path, description)
    return analysis

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот, который может отвечать на текстовые запросы, генерировать изображения и анализировать фото. Отправьте текст или изображение с описанием.')

def handle_message(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    if "нарисуй" in query.lower():
        image_url = generate_image(query)
        update.message.reply_text(f'Вот ваше изображение: {image_url}')
    else:
        response = handle_text_request(query)
        update.message.reply_text(response)

def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()
    photo_path = photo_file.download()
    description = update.message.caption if update.message.caption else "анализировать"
    analysis = analyze_photo(photo_path, description)
    update.message.reply_text(analysis)

def main():
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    updater.start_polling()
    updater.idle()

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

