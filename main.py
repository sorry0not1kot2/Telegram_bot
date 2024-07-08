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

# Список провайдеров из репозитория gpt4free
available_providers = [
    "You", "Forefront", "DeepAI", "ChatGPT", "OpenAI", "Anthropic", "Cohere", "AI21", "AlephAlpha"
]
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
    if not context.args:
        provider_list = "\n".join([f"{i+1}. {provider}" for i, provider in enumerate(available_providers)])
        await update.message.reply_text(f"Пожалуйста, укажите номер одного из доступных провайдеров:\n{provider_list}")
        return

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
    
# конец

