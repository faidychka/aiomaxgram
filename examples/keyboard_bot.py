"""
Пример бота с интерактивной клавиатурой для Max

Этот бот отправляет сообщение с кнопками и обрабатывает нажатия на них.
"""

import asyncio
import logging
import os
from maxgram import Bot

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получение токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("Пожалуйста, установите переменную окружения MAX_BOT_TOKEN")
    exit(1)

# Инициализация бота
bot = Bot(TOKEN)

# Создание клавиатуры
def get_keyboard():
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {"type": "callback", "text": "Кнопка 1", "payload": "button1"}
                ],
                [
                    {"type": "callback", "text": "Кнопка 2", "payload": "button2"},
                    {"type": "callback", "text": "Кнопка 3", "payload": "button3"}
                ],
                [
                    {"type": "link", "text": "Открыть ссылку", "url": "https://max.ru"}
                ]
            ]
        }
    }

# Обработчик события запуска бота
@bot.on("bot_started")
def on_start(ctx):
    ctx.reply(
        "Привет! Я бот с клавиатурой. Нажми на одну из кнопок ниже:",
        attachments=[get_keyboard()]
    )

# Обработчик команды '/keyboard'
@bot.command("keyboard")
def keyboard_command(ctx):
    ctx.reply(
        "Вот клавиатура. Выбери одну из опций:",
        attachments=[get_keyboard()]
    )

# Обработчик нажатий на кнопки
@bot.on("message_callback")
def handle_callback(ctx):
    payload = ctx.payload
    
    if payload == "button1":
        ctx.answer_callback("Вы нажали на кнопку 1")
        ctx.reply("Вы выбрали первую опцию")
    elif payload == "button2":
        ctx.answer_callback("Вы нажали на кнопку 2")
        ctx.reply("Вы выбрали вторую опцию")
    elif payload == "button3":
        ctx.answer_callback("Вы нажали на кнопку 3")
        ctx.reply("Вы выбрали третью опцию")
    else:
        ctx.answer_callback(f"Неизвестная кнопка: {payload}")

# Запуск бота
if __name__ == "__main__":
    try:
        logger.info("Запуск бота...")
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
        bot.stop()
        logger.info("Бот остановлен") 