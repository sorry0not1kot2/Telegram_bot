# 
#
#
# файл mmain.py
import os
import asyncio
import logging
import json
from telebot.async_telebot import AsyncTeleBot
import g4f

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, 'Привет! Я бот для общения с LLM GPT-4o.')

# Словарь для хранения истории чата
chat_history = {}

# Асинхронная функция для обработки сообщений
@bot.message_handler(content_types=['text'])
async def handle_message(message):
    try:
        user_id = message.chat.id
        user_message = message.text
        
        logging.info(f"Получено сообщение: {user_message}")
        
        # Инициализация истории чата для нового пользователя
        if user_id not in chat_history:
            chat_history[user_id] = []

        # Добавление сообщения пользователя в историю чата
        chat_history[user_id].append({"role": "user", "content": user_message})
        
        logging.info(f"Отправка запроса к g4f")
        response = g4f.ChatCompletion.create(
            model="gpt-4o",
            messages=chat_history[user_id],
            no_sandbox=True
        )
        
        logging.info(f"Получен ответ от g4f: {response}")
        
        # Проверка на пустой ответ
        if not response:
            logging.warning("Получен пустой ответ от g4f")
            await bot.send_message(message.chat.id, "Извините, я не смог сгенерировать ответ. Попробуйте еще раз.")
            return
        
        if isinstance(response, str):
            try:
                response_data = json.loads(response)
                bot_response = response_data['choices'][0]['message']['content']
            except json.JSONDecodeError:
                bot_response = response  # Используем ответ как есть, если это не JSON
        elif isinstance(response, dict):
            bot_response = response.get('choices', [{}])[0].get('message', {}).get('content', 'Нет ответа')
        else:
            raise ValueError("Неожиданный формат ответа от API")
        
        # Добавление ответа бота в историю чата
        chat_history[user_id].append({"role": "assistant", "content": bot_response})
        
        await bot.send_message(message.chat.id, bot_response)
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения: {e}")
        await bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего сообщения.")

# Асинхронная функция main для запуска бота
async def main():
    while True:
        try:
            logging.info("Бот запущен")
            await bot.polling(non_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в основном цикле бота: {e}")
            await asyncio.sleep(5)  # Пауза перед повторной попыткой

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())

"""
# Список провайдеров и моделей
provider_models = {
    "You": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    "Forefront": ["claude-v1", "claude-v1.3"],
    "DeepAI": ["deepai-gpt", "deepai-gpt-4"]
}
"""

# конец

