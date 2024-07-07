# 
#
#
# файл mmain.py

# Код с провайдерами и моделями бесплатно с g4f. 
# без библиотеки siogram Файл main.py:
# Исправленная версия, работает с асинхронными функциями и телебот без аиограм

import os
import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import g4f
from g4f import Provider

# Настройка бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Отсутствует переменная окружения TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(bot=bot)
dispatcher = updater.dispatcher

user_contexts = {}

available_providers = [provider.name for provider in Provider.Providers]
provider_models = {
    "You": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    "Forefront": ["claude-v1", "claude-v1.3"],
    "DeepAI": ["deepai-gpt", "deepai-gpt-4"],
    # Добавьте другие провайдеры и модели здесь
}

def get_llm_response(prompt, context, provider_name, model_name):
    full_prompt = context + "\n" + prompt if context else prompt

    provider = next((p for p in Provider.Providers if p.name == provider_name), None)
    if provider is None:
        raise ValueError(f"Provider {provider_name} not found")

    response = g4f.ChatCompletion.create(
        provider=provider,
        model=model_name,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response['choices'][0]['message']['content']

def start(update: Update, context: CallbackContext):
    user_contexts[update.message.chat_id] = {"context": "", "provider": "", "model": ""}
    context.bot.send_message(chat_id=update.message.chat_id, text="Привет! Я бот, использующий GPT-4. Сначала выберите провайдера, используя команду /setprovider.")

def set_provider(update: Update, context: CallbackContext):
    provider = context.args[0] if context.args else None
    if provider and provider in available_providers:
        user_contexts[update.message.chat_id]["provider"] = provider
        user_contexts[update.message.chat_id]["model"] = ""  # Сбросить выбранную модель при смене провайдера
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Провайдер установлен на {provider}. Теперь выберите модель, используя команду /setmodel.")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Пожалуйста, укажите одного из доступных провайдеров: {', '.join(available_providers)}")

def set_model(update: Update, context: CallbackContext):
    provider = user_contexts[update.message.chat_id]["provider"]
    model = context.args[0] if context.args else None

    if not provider:
        context.bot.send_message(chat_id=update.message.chat_id, text="Сначала выберите провайдера, используя команду /setprovider.")
        return

    if model and model in provider_models.get(provider, []):
        user_contexts[update.message.chat_id]["model"] = model
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Модель установлена на {model}.")
    else:
        available_models = provider_models.get(provider, [])
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Пожалуйста, укажите одну из доступных моделей для провайдера {provider}: {', '.join(available_models)}")

def reset_context(update: Update, context: CallbackContext):
    user_contexts[update.message.chat_id] = {"context": "", "provider": "", "model": ""}
    context.bot.send_message(chat_id=update.message.chat_id, text="Контекст сброшен. Пожалуйста, выберите провайдера, используя команду /setprovider.")

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    user_data = user_contexts.get(user_id, {"context": "", "provider": "", "model": ""})
    context = user_data["context"]
    provider = user_data["provider"]
    model = user_data["model"]

    if not provider:
        context.bot.send_message(chat_id=update.message.chat_id, text="Сначала выберите провайдера, используя команду /setprovider.")
        return

    if not model:
        context.bot.send_message(chat_id=update.message.chat_id, text="Сначала выберите модель, используя команду /setmodel.")
        return

    response = get_llm_response(update.message.text, context, provider, model)
    
    user_contexts[user_id]["context"] = context + "\nUser: " + update.message.text + "\nBot: " + response
    context.bot.send_message(chat_id=update.message.chat_id, text=response)

if __name__ == '__main__':
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("setprovider", set_provider))
    dispatcher.add_handler(CommandHandler("setmodel", set_model))
    dispatcher.add_handler(CommandHandler("reset", reset_context))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    updater.start_polling()
    updater.idle()
    
# конец

