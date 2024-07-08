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
available_providers = [provider for provider in dir(providers) if callable(getattr(providers, provider)) and not provider.startswith("__")]
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
    if context.args:
        try:
            model_index = int(context.args[0]) - 1
            all_models = [model for models in provider_models.values() for model in models]
            
            if 0 <= model_index < len(all_models):
                model = all_models[model_index]
                user_contexts[update.message.chat_id]["model"] = model
                await update.message.reply_text(f"Модель установлена на {model}. Теперь выберите провайдера, используя команду /setprovider.")
                return
        except ValueError:
            pass

    model_list = "\n".join([f"{i+1}. {model}" for i, model in enumerate([model for models in provider_models.values() for model in models])])
    await update.message.reply_text(f"Пожалуйста, укажите номер одной из доступных моделей:\n{model_list}")

async def set_provider(update: Update, context: CallbackContext):
    if context.args:
        try:
            provider_index = int(context.args[0]) - 1
            
            if 0 <= provider_index < len(available_providers):
                provider = available_providers[provider_index]
                user_contexts[update.message.chat_id]["provider"] = provider
                await update.message.reply_text(f"Провайдер установлен на {provider}. Теперь вы можете отправить сообщение.")
                return
        except ValueError:
            pass

    provider_list = "\n".join([f"{i+1}. {provider}" for i, provider in enumerate(available_providers)])
    await update.message.reply_text(f"Пожалуйста, укажите номер одного из доступных провайдеров:\n{provider_list}")

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

