import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import ChatCompletion, Provider

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Получение имени пользователя бота
bot_info = asyncio.run(bot.get_me())
bot_username = bot_info.username

# Обработчик сообщений
@bot.message_handler(func=lambda message: bot_username in message.text or (
        message.reply_to_message and message.reply_to_message.from_user.username == bot_username))
async def handle_message(message):
    query = message.text.replace(f"@{bot_username}", "").strip()

    if query:
        logger.info(f"Получен запрос: {query}")
        await bot.send_message(message.chat.id, "Обрабатываю ваш запрос...")

        try:
            # Отправка запроса к Bing Chat
            response = await ChatCompletion.create_async(
                model="bing",  # Используем модель "bing"
                provider=Provider.Bing, # Используем провайдера Bing
                messages=[{"role": "user", "content": query}]
            )

            # Отправка ответа пользователю
            chat_gpt_response = response.choices[0].message.content
            await bot.reply_to(message, chat_gpt_response, parse_mode="MarkdownV2")
            logger.info("Ответ отправлен")

        except Exception as e:
            logger.exception(f"Ошибка при обработке запроса:")
            await bot.reply_to(message, "Извините, произошла ошибка.")
    else:
        await bot.reply_to(message, "Введите сообщение.")


# Функция для запуска бота
async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(none_stop=True)
    except Exception as e:
        logger.exception(f"Ошибка при работе бота:")


# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
