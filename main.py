"""
import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import Provider, ChatCompletion

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = AsyncTeleBot(BOT_TOKEN)

# Хранение данных по разговорам
conversation_data = {}

# Получение имени пользователя бота
bot_info = asyncio.run(bot.get_me())
bot_username = bot_info.username

# Функция для получения ответа от GPT-4 через Claude-3-Sonnet
async def get_gpt_response(query):
    try:
        response = ChatCompletion.create(
            provider=Provider.You,
            model='claude-3-sonnet',
            messages=[{"role": "user", "content": query}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

@bot.message_handler(commands=['start'])
async def handle_start_command(message):
    await bot.send_message(message.chat.id, f"Привет! Я - GPT-бот. Обращайтесь по @{bot_username} или отвечайте на мои сообщения, чтобы получить ответ.")

@bot.message_handler(commands=['clear'])
async def handle_clear_command(message):
    conversation_data.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "Данные очищены.")

@bot.message_handler(func=lambda message: bot_username in message.text or (message.reply_to_message and message.reply_to_message.from_user.username == bot_username))
async def handle_message(message):
    query = message.text.replace(f"@{bot_username}", "").strip()
    
    if query:
        logger.info(f"Получен запрос: {query}")
        await bot.send_message(message.chat.id, "Обрабатываю ваш запрос...")
        
        # Используем get_gpt_response для получения ответа от Claude-3-Sonnet
        response = await get_gpt_response(query)
        
        await bot.reply_to(message, response)
        logger.info("Ответ отправлен")
    else:
        await bot.reply_to(message, "Введите сообщение.")

# Функция для запуска бота
async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {str(e)}")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
"""

import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import Provider, ChatCompletion

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Не установлен TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(BOT_TOKEN)

# Получение имени пользователя бота
bot_info = asyncio.run(bot.get_me())
bot_username = bot_info.username

# Хранение данных по разговорам (инициализация)
conversation_data = {}

# Функция для получения ответа от GPT-4 через Claude-3-Sonnet
async def get_gpt_response(query):
    try:
#        response = await ChatCompletion.create(
#            provider=Provider.Bing,
#            model='gpt-4',
#            messages=[{"role": "user", "content": query}]
#        ) 

        response = await ChatCompletion.create(
            provider=Provider.GeekGpt,
            model='gpt-4',
            messages=[{"role": "user", "content": query}]
        )
#        response = await ChatCompletion.create(
#            provider=Provider.GeekGpt,
#            model='gpt-4',
#            messages=[{"role": "user", "content": query}]
#        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

@bot.message_handler(commands=['start'])
async def handle_start_command(message):
    await bot.send_message(message.chat.id, f"Привет! Я - GPT-бот. Обращайтесь по @{bot_username} или отвечайте на мои сообщения, чтобы получить ответ.")

@bot.message_handler(commands=['clear'])
async def handle_clear_command(message):
    conversation_data.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "Данные очищены.")

@bot.message_handler(func=lambda message: bot_username in message.text or (message.reply_to_message and message.reply_to_message.from_user.username == bot_username))
async def handle_message(message):
    query = message.text.replace(f"@{bot_username}", "").strip()
    
    if query:
        logger.info(f"Получен запрос: {query}")
        await bot.send_message(message.chat.id, "Обрабатываю ваш запрос...")
        
        # Используем get_gpt_response для получения ответа от Claude-3-Sonnet
        response = await get_gpt_response(query)
        
        await bot.reply_to(message, response)
        logger.info("Ответ отправлен")
    else:
        await bot.reply_to(message, "Введите сообщение.")

# Функция для запуска бота

Try Pro
Upgrade for image upload, smarter AI, and more Pro Search.
User avatar
doczivag
37m
На русском как это сделать:g4f.cookies.set_cookies() response = g4f.ChatCompletion.create( model=g4f.models.gpt_4, messages=[{"role": "user", "content": "Привет, как дела?"}], provider=provider ) response.choices[0].message.content)
На русском как это сделать:g4f.cookies.set_cookies()

response = g4f.ChatCompletion.create( model=g4f.models.gpt_4, messages=[{"role": "user", "content": "Привет, как дела?"}], provider=provider )


response.choices[0].message.content)
Answer
Вот как это сделать на русском языке:
python
import g4f

g4f.cookies.set_cookies()

response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Привет, как дела?"}],
    provider=provider
)

print(response.choices[0].message.content)

Объяснение:
Сначала мы импортируем модуль g4f, который предоставляет API для работы с Anthropic GPT-4.
Вызываем g4f.cookies.set_cookies(), чтобы установить необходимые файлы cookie для аутентификации.
Создаем запрос к API чата Anthropic с помощью g4f.ChatCompletion.create():
Указываем модель g4f.models.gpt_4, которую будем использовать (в данном случае GPT-4).
Формируем список сообщений messages, где первое сообщение от пользователя с текстом "Привет, как дела?".
Передаем provider, который содержит информацию об аутентификации (не показан в примере).
Наконец, выводим содержимое ответа от модели с помощью print(response.choices.message.content).
Этот код отправляет запрос к API чата Anthropic с использованием GPT-4, передавая сообщение от пользователя, и выводит ответ модели в консоль.
Какие модели поддерживаются в g4f.models.gpt_4
Sources



qna.habr.com favicon
gitee.com favicon
View 2 more
Answer
В модуле g4f.models в библиотеке g4f поддерживаются следующие модели:
GPT-4: Это основная модель, которая используется для создания чата и ответов на вопросы.
GPT-3.5 Turbo: Это более мощная версия GPT-3.5, которая обеспечивает более быстрый и более точный ответ.
GPT-4o: Это дополнительная модель, которая может быть использована для создания чата с использованием gpt-4o в chat.completion.create.
Вот пример использования модели GPT-4 для создания чата:
python
import g4f

response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Привет, как дела?"}],
    provider=g4f.Provider.ChatgptAi
)

print(response.choices[0].message.content)

В этом примере мы создаем чат с использованием модели GPT-4 и провайдера ChatgptAi. Затем мы выводим содержимое ответа модели в консоль.
github.com
freegpttools.org
github.com
github.com
pub.towardsai.net
pypi.org
researchgate.net
View More
Какие провайдеры используются для gpt-4 в g4f
Sources



qna.habr.com favicon
pypi.org favicon
View 2 more
Answer
В библиотеке g4f для работы с моделью GPT-4 поддерживаются следующие провайдеры:
Bing: g4f.Provider.Bing
ChatgptAi: g4f.Provider.ChatgptAi
Liaobots: g4f.Provider.Liaobots
Raycast: g4f.Provider.Raycast
Для использования этих провайдеров необходимо передать соответствующий провайдер в параметре provider при создании чата:
python
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "Привет, как дела?"}],
    provider=g4f.Provider.Bing
)

Стоит отметить, что для провайдера Bing может потребоваться прокси или VPN, так как он является одним из самых стабильных и постоянно работающих провайдеров GPT-4.
Какие провайдеры для GPT-4 в g4f предлагают бесплатный доступ
Sources



blast.hk favicon
pikabu.ru favicon
View 2 more
Answer
Согласно поисковым результатам, в библиотеке g4f для работы с моделью GPT-4 поддерживаются следующие бесплатные провайдеры:
GeekGpt: g4f.Provider.GeekGpt 
ChatgptAi: g4f.Provider.ChatgptAi 
Эти провайдеры позволяют получить бесплатный доступ к GPT-4 через библиотеку g4f. Однако, как отмечается в статьях, для использования провайдера GeekGpt может потребоваться настройка прокси-сервера, чтобы обойти ограничения .
Также в поисковых результатах упоминается, что библиотека g4f поддерживает использование прокси в целом, что может быть полезно для получения стабильного доступа к GPT-4 через различные провайдеры .
Таким образом, g4f.Provider.GeekGpt и g4f.Provider.ChatgptAi являются двумя бесплатными провайдерами GPT-4, доступными в библиотеке g4f, хотя для некоторых из них может потребоваться дополнительная настройка.
А есть бесплатный gpt-4o и Claude sonnet
Sources



habr.com favicon
pypi.org favicon
View 2 more
Answer
К сожалению, в результатах поиска не было найдено информации о бесплатном доступе к моделям GPT-4o или Claude sonnet в библиотеке g4f.
Согласно документации g4f, поддерживаются следующие модели:
GPT-4: Основная модель, используемая для создания чатов и ответов на вопросы.
GPT-3.5 Turbo: Более мощная версия GPT-3.5, обеспечивающая более быстрые и точные ответы.
GPT-4o: Дополнительная модель, которую можно использовать для создания чатов с помощью gpt-4o в chat.completion.create.
Однако в результатах поиска не было найдено информации о бесплатном доступе к модели GPT-4o или Claude sonnet через библиотеку g4f.
Большинство провайдеров, поддерживаемых g4f, предоставляют бесплатный доступ к GPT-3.5, но не к более мощным моделям, таким как GPT-4. Для получения доступа к GPT-4 может потребоваться платная подписка или использование других сервисов, не связанных с g4f.
Таким образом, на основе доступной информации, я не могу подтвердить наличие бесплатного доступа к моделям GPT-4o или Claude sonnet через библиотеку g4f. Извините, что не могу предоставить более подробную информацию по этому запросу.
github.com
kdnuggets.com
reddit.com
synced.sg
snyk.io
Какие провайдеры для GPT-4 в g4f предлагают наилучшие условия для бесплатного использования
Sources



vc.ru favicon
blast.hk favicon
View 2 more
Answer
На основе анализа поисковых результатов, можно выделить следующие провайдеры в библиотеке g4f, которые предлагают наилучшие условия для бесплатного использования GPT-4:
GeekGpt
Провайдер g4f.Provider.GeekGpt позволяет получить бесплатный доступ к GPT-4 через библиотеку g4f.
Однако, для использования этого провайдера может потребоваться настройка прокси-сервера, чтобы обойти ограничения.
ChatgptAi
Провайдер g4f.Provider.ChatgptAi также предоставляет бесплатный доступ к GPT-4 в g4f.
Этот провайдер считается одним из самых стабильных и постоянно работающих для бесплатного использования GPT-4.
Стоит отметить, что для обоих провайдеров может потребоваться дополнительная настройка, например, использование прокси, чтобы обеспечить стабильный доступ к GPT-4.
Другие провайдеры, такие как g4f.Provider.Bing и g4f.Provider.Raycast, также поддерживают GPT-4, но информация о бесплатном доступе к ним в g4f отсутствует.
Таким образом, g4f.Provider.GeekGpt и g4f.Provider.ChatgptAi являются наиболее подходящими провайдерами для бесплатного использования GPT-4 в библиотеке g4f, хотя для их использования может потребоваться дополнительная настройка.
Какие сервисы работают с GPT-4 бесплатно и безопасно
Sources



vc.ru favicon
vc.ru favicon
View 2 more
Answer
Согласно поисковым результатам, существует несколько сервисов, которые предоставляют бесплатный доступ к GPT-4 с различными ограничениями:
HuggingFace
Платформа, предоставляющая доступ к различным языковым моделям, включая GPT-4.
Доступны модели gpt4-large, gpt4-medium и gpt4-small для использования онлайн, скачивания или через API.
Имеет бесплатный план для небольших проектов с лимитом 2 часов вычислений в месяц.
GeekGpt
Провайдер g4f.Provider.GeekGpt в библиотеке g4f позволяет получить бесплатный доступ к GPT-4.
Может потребоваться настройка прокси для обхода ограничений.
ChatgptAi
Провайдер g4f.Provider.ChatgptAi в g4f также предоставляет бесплатный доступ к GPT-4.
Считается одним из самых стабильных и постоянно работающих бесплатных провайдеров GPT-4.
Ora
Веб-платформа, где можно собрать свою ИИ-модель, включая GPT-4, после регистрации.
Telegram-бот
Бесплатный бот в Telegram, доступный по ссылке https://t.me/NB_GPT4_bot.
Требует подписки на 2 канала для использования GPT-4 с ограничениями.
Стоит отметить, что для некоторых сервисов может потребоваться дополнительная настройка, например использование прокси, чтобы обеспечить стабильный доступ к GPT-4. Также следует учитывать возможные ограничения в объеме запросов и функциональности при бесплатном использовании.
Есть ли сервисы, которые не требуют регистрации для использования GPT-4 бесплатно
Sources



lred.ru favicon
habr.com favicon
View 2 more
Answer
Да, есть несколько сервисов, которые позволяют использовать GPT-4 бесплатно без необходимости регистрации:
Telegram-бот
Бесплатный бот в Telegram, доступный по ссылке https://t.me/NB_GPT4_bot[2].
Для использования GPT-4 требуется подписаться на 2 канала, после чего можно пользоваться с ограничениями.
Nova
Мобильное приложение, использующее GPT-4.
При запуске приложения предлагается оформить платную подписку, но ее можно закрыть крестиком в левом верхнем углу.
После этого доступен бот "GPT-4" с одним бесплатным запросом в сутки.
Bing
Чат-бот Bing по умолчанию использует GPT-4.
Можно просто зайти в чат и начать пользоваться, но будут действовать некоторые ограничения.
Таким образом, Telegram-бот, Nova и Bing позволяют использовать GPT-4 бесплатно без необходимости регистрации, хотя и с определенными ограничениями. Другие сервисы, такие как HuggingFace, GeekGpt, ChatgptAi и Ora, также предоставляют бесплатный доступ к GPT-4, но требуют предварительной регистрации.
import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import Provider, ChatCompletion

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка бота
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("Не установлен TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(BOT_TOKEN)

# Получение имени пользователя бота
bot_info = asyncio.run(bot.get_me())
bot_username = bot_info.username

# Хранение данных по разговорам (инициализация)
conversation_data = {}

# Функция для получения ответа от GPT-4 через Claude-3-Sonnet
async def get_gpt_response(query):
    try:
        response = await ChatCompletion.create(
            provider=Provider.Bing,
            model='gpt-4',
            messages=[{"role": "user", "content": query}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от GPT: {str(e)}")
        return f"Ошибка при получении ответа от GPT: {str(e)}"

@bot.message_handler(commands=['start'])
async def handle_start_command(message):
    await bot.send_message(message.chat.id, f"Привет! Я - GPT-бот. Обращайтесь по @{bot_username} или отвечайте на мои сообщения, чтобы получить ответ.")

@bot.message_handler(commands=['clear'])
async def handle_clear_command(message):
    conversation_data.pop(message.chat.id, None)
    await bot.send_message(message.chat.id, "Данные очищены.")

@bot.message_handler(func=lambda message: bot_username in message.text or (message.reply_to_message and message.reply_to_message.from_user.username == bot_username))
async def handle_message(message):
    query = message.text.replace(f"@{bot_username}", "").strip()
    
    if query:
        logger.info(f"Получен запрос: {query}")
        await bot.send_message(message.chat.id, "Обрабатываю ваш запрос...")
        
        # Используем get_gpt_response для получения ответа от Claude-3-Sonnet
        response = await get_gpt_response(query)
        
        await bot.reply_to(message, response)
        logger.info("Ответ отправлен")
    else:
        await bot.reply_to(message, "Введите сообщение.")

# Функция для запуска бота
async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(non_stop=True, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {str(e)}")

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
Answer
Это код бота для Telegram, написанный на Python, который использует библиотеку telebot для асинхронного взаимодействия с Telegram API и библиотеку g4f для взаимодействия с моделью GPT-4 от Anthropic.
Основные функции бота:
Обработка команды /start: Бот отправляет приветственное сообщение при запуске.
Обработка команды /clear: Бот очищает данные разговора пользователя.
Обработка сообщений: Бот реагирует на сообщения, в которых упоминается его username или на сообщения, являющиеся ответом на его сообщения. Он отправляет запрос к GPT-4 через библиотеку g4f и отправляет ответ пользователю.
Код также включает в себя:
Настройку логирования для отслеживания ошибок и информационных сообщений.
Получение username бота для корректной обработки сообщений.
Хранение данных по разговорам (в данном случае просто инициализируется).
Функцию для получения ответа от GPT-4 через провайдер Bing.
Для работы бота необходимо установить следующие зависимости:
telebot (библиотека для работы с Telegram API)
g4f (библиотека для работы с моделью GPT-4 от Anthropic)
Также требуется установить переменную окружения TELEGRAM_BOT_TOKEN со значением токена вашего бота в Telegram.
Запуск бота осуществляется с помощью функции main(), которая использует asyncio для асинхронной работы.
Подставить в программу другого бесплатного провайдера
Sources



docs.python.org favicon
superfastpython.com favicon
View 2 more
Answer
Чтобы подставить другого бесплатного провайдера вместо Bing в приведенном коде бота для Telegram, нужно изменить строку:
python
response = await ChatCompletion.create(
    provider=Provider.Bing,
    model='gpt-4',
    messages=[{"role": "user", "content": query}]
)

Вместо Provider.Bing можно использовать другого провайдера, например Provider.GeekGpt:
python
response = await ChatCompletion.create(
    provider=Provider.GeekGpt,
    model='gpt-4',
    messages=[{"role": "user", "content": query}]
)

Или Provider.ChatgptAi:
python
response = await ChatCompletion.create(
    provider=Provider.ChatgptAi,
    model='gpt-4',
    messages=[{"role": "user", "content": query}]
)

Однако стоит учитывать, что для некоторых провайдеров, таких как Provider.GeekGpt, может потребоваться дополнительная настройка, например использование прокси, чтобы обеспечить стабильный доступ к GPT-4.
Также важно следить за возможными ограничениями в объеме запросов и функциональности при бесплатном использовании различных провайдеров.
build
Started 1m 48s ago
Search logs
0s
1s
0s
7s
1m 40s
Run set -x  # Включить вывод команд
+ python main.py
ERROR:asyncio:Fatal error on SSL transport
protocol: <asyncio.sslproto.SSLProtocol object at 0x7f3dc9db5b10>
transport: <_SelectorSocketTransport closing fd=6>
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/selector_events.py", line 924, in write
    n = self._sock.send(data)
OSError: [Errno 9] Bad file descriptor
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/sslproto.py", line 690, in _process_write_backlog
    self._transport.write(chunk)
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/selector_events.py", line 930, in write
    self._fatal_error(exc, 'Fatal write error on socket transport')
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/selector_events.py", line 725, in _fatal_error
    self._force_close(exc)
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/selector_events.py", line 737, in _force_close
    self._loop.call_soon(self._call_connection_lost, exc)
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/base_events.py", line 753, in call_soon
    self._check_closed()
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/base_events.py", line 515, in _check_closed
Error:     raise RuntimeError('Event loop is closed')
RuntimeError: Event loop is closed
Answer
Похоже, что в коде бота возникла ошибка при работе с асинхронным событийным циклом (event loop) библиотеки asyncio. Ошибка "Event loop is closed" обычно возникает, когда вы пытаетесь выполнить асинхронные операции после закрытия цикла событий.
Чтобы исправить ошибку, попробуйте внести следующие изменения в код:
Измените функцию main() так, чтобы она не использовала asyncio.run():
python
async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(non_stop=True, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {str(e)}")

Добавьте следующий код в конец файла, чтобы запустить бота:
python
if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")

Теперь код должен выглядеть так:
python
import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import Provider, ChatCompletion

# ... (остальной код без изменений)

async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(non_stop=True, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {str(e)}")

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")

Эти изменения должны помочь избежать ошибки "Event loop is closed" и стабилизировать работу бота.
Также убедитесь, что вы используете актуальные версии библиотек telebot и g4f, так как ошибки могут быть связаны с несовместимостью версий.
File "/home/runner/work/Telegram_bot/Telegram_bot/main.py", line 157, in <module>
    loop = asyncio.get_event_loop()
  File "/opt/hostedtoolcache/Python/3.10.14/x64/lib/python3.10/asyncio/events.py", line 656, in get_event_loop
    raise RuntimeError('There is no current event loop in thread %r.'
RuntimeError: There is no current event loop in thread 'MainThread'.
ERROR:asyncio:Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x7f21dacb18a0>
ERROR:asyncio:Unclosed connector
connections: ['[(<aiohttp.client_proto.ResponseHandler object at 0x7f21dac99d20>, 239.42264093)]']
connector: <aiohttp.connector.TCPConnector object at 0x7f21dacb1810>
Error: Process completed with exit code 1.
Answer
Похоже, что возникла еще одна ошибка, связанная с асинхронным событийным циклом. Ошибка "There is no current event loop in thread 'MainThread'" указывает на то, что в основном потоке (MainThread) нет активного событийного цикла.
Чтобы исправить это, вам нужно создать и запустить событийный цикл явно в основном потоке. Вот как можно это сделать:
python
import asyncio
import logging
import os
from telebot.async_telebot import AsyncTeleBot
from g4f import Provider, ChatCompletion

# ... (остальной код без изменений)

async def main():
    try:
        logger.info("Запуск бота...")
        await bot.polling(non_stop=True, timeout=60)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {str(e)}")

if __name__ == '__main__':
    # Создаем и запускаем событийный цикл
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    finally:
        # Закрываем событийный цикл
        loop.close()
