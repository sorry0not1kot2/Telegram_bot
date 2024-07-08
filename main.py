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
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import g4f
from g4f import providers

# Настройка бота
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Отсутствует переменная окружения TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Создание приложения
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

user_contexts = {}

# Фильтрация провайдеров, чтобы включить только те, которые могут быть использованы для генерации текста
available_providers = [provider for provider in dir(providers) if provider not in ["base_provider", "helper", "retry_provider", "types"]]
provider_models = {
    "You": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    "Forefront": ["claude-v1", "claude-v1.3"],
    "DeepAI": ["deepai-gpt", "deepai-gpt-4"],
    # Добавьте другие провайдеры и модели здесь
}

def get_llm_response(prompt, context, provider_name, model_name):
    full_prompt = context + "\n" + prompt if context else prompt

    provider = getattr(providers, provider_name, None)
    if provider is None:
        raise ValueError(f"Provider {provider_name} not found")

    response = g4f.ChatCompletion.create(
        provider=provider,
        model=model_name,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response['choices'][0]['message']['content']

async def start(update: Update, context: CallbackContext):
    user_contexts[update.message.chat_id] = {"context": "", "provider": "", "model": ""}
    await update.message.reply_text("Привет! Я бот, использующий GPT-4. Сначала выберите модель, используя команду /setmodel.")

async def set_model(update: Update, context: CallbackContext):
    model = context.args[0] if context.args else None
    if model and any(model in models for models in provider_models.values()):
        user_contexts[update.message.chat_id]["model"] = model
        await update.message.reply_text(f"Модель установлена на {model}. Теперь выберите провайдера, используя команду /setprovider.")
    else:
        all_models = [model for models in provider_models.values() for model in models]
        await update.message.reply_text(f"Пожалуйста, укажите одну из доступных моделей: {', '.join(all_models)}")

async def set_provider(update: Update, context: CallbackContext):
    provider = context.args[0] if context.args else None
    if provider and provider in available_providers:
        user_contexts[update.message.chat_id]["provider"] = provider
        await update.message.reply_text(f"Провайдер установлен на {provider}. Теперь вы можете отправить сообщение.")
    else:
        await update.message.reply_text(f"Пожалуйста, укажите одного из доступных провайдеров: {', '.join(available_providers)}")

async def reset_context(update: Update, context: CallbackContext):
    user_contexts[update.message.chat_id] = {"context": "", "provider": "", "model": ""}
    await update.message.reply_text("Контекст сброшен. Пожалуйста, выберите модель, используя команду /setmodel.")

async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.chat_id
    user_data = user_contexts.get(user_id, {"context": "", "provider": "", "model": ""})
    user_context = user_data["context"]
    provider = user_data["provider"]
    model = user_data["model"]

    if not model:
        await update.message.reply_text("Сначала выберите модель, используя команду /setmodel.")
        return

    if not provider:
        await update.message.reply_text("Сначала выберите провайдера, используя команду /setprovider.")
        return

    response = get_llm_response(update.message.text, user_context, provider, model)
    
    user_contexts[user_id]["context"] = user_context + "\nUser: " + update.message.text + "\nBot: " + response
    await update.message.reply_text(response)

if __name__ == '__main__':
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setmodel", set_model))
    application.add_handler(CommandHandler("setprovider", set_provider))
    application.add_handler(CommandHandler("reset", reset_context))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

# конец

