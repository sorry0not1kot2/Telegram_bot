# 
#
#
# файл mmain.py


# Код с провайдерами и моделями бесплатно с g4f. 
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import g4f
from g4f.Provider import Providers

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Отсутствует переменная окружения TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

user_contexts = {}

available_providers = [provider.name for provider in Providers]
provider_models = {
    "You": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    "Forefront": ["claude-v1", "claude-v1.3"],
    "DeepAI": ["deepai-gpt", "deepai-gpt-4"],
    # Добавьте другие провайдеры и модели здесь
}

async def get_llm_response(prompt, context, provider_name, model_name):
    full_prompt = context + "\n" + prompt if context else prompt

    provider = next((p for p in Providers if p.name == provider_name), None)
    if provider is None:
        raise ValueError(f"Provider {provider_name} not found")

    response = await g4f.ChatCompletion.create(
        provider=provider,
        model=model_name,
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response['choices'][0]['message']['content']

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_contexts[message.from_user.id] = {"context": "", "provider": "", "model": ""}
    await message.reply("Привет! Я бот, использующий GPT-4. Сначала выберите провайдера, используя команду /setprovider.")

@dp.message_handler(commands=['setprovider'])
async def set_provider(message: types.Message):
    provider = message.text.split()[1] if len(message.text.split()) > 1 else None
    if provider and provider in available_providers:
        user_contexts[message.from_user.id]["provider"] = provider
        user_contexts[message.from_user.id]["model"] = ""  # Сбросить выбранную модель при смене провайдера
        await message.reply(f"Провайдер установлен на {provider}. Теперь выберите модель, используя команду /setmodel.")
    else:
        await message.reply(f"Пожалуйста, укажите одного из доступных провайдеров: {', '.join(available_providers)}")

@dp.message_handler(commands=['setmodel'])
async def set_model(message: types.Message):
    user_id = message.from_user.id
    provider = user_contexts[user_id]["provider"]
    model = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not provider:
        await message.reply("Сначала выберите провайдера, используя команду /setprovider.")
        return

    if model and model in provider_models.get(provider, []):
        user_contexts[user_id]["model"] = model
        await message.reply(f"Модель установлена на {model}.")
    else:
        available_models = provider_models.get(provider, [])
        await message.reply(f"Пожалуйста, укажите одну из доступных моделей для провайдера {provider}: {', '.join(available_models)}")

@dp.message_handler(commands=['reset'])
async def reset_context(message: types.Message):
    user_contexts[message.from_user.id] = {"context": "", "provider": "", "model": ""}
    await message.reply("Контекст сброшен. Пожалуйста, выберите провайдера, используя команду /setprovider.")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_data = user_contexts.get(user_id, {"context": "", "provider": "", "model": ""})
    context = user_data["context"]
    provider = user_data["provider"]
    model = user_data["model"]

    if not provider:
        await message.reply("Сначала выберите провайдера, используя команду /setprovider.")
        return

    if not model:
        await message.reply("Сначала выберите модель, используя команду /setmodel.")
        return

    response = await get_llm_response(message.text, context, provider, model)
    
    user_contexts[user_id]["context"] = context + "\nUser: " + message.text + "\nBot: " + response

    await message.reply(response, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

# конец

