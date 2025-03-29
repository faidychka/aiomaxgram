"""
Пример бота с интерактивной клавиатурой для Max

Этот бот отправляет сообщение с кнопками и обрабатывает нажатия на них.
"""

import logging
import os
from maxgram import Bot
from maxgram.keyboards import InlineKeyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получение токена из переменной окружения
TOKEN = "f9LHodD0cOLxCsVYq1ooE9uDuaMrtazHuNBTkmlC8DbIrQ4hXs5UedYzgcTma3JSZHR3W_hlxwYv3ySlopom"
if not TOKEN:
    logger.error("Пожалуйста, установите переменную окружения MAX_BOT_TOKEN")
    exit(1)

# Инициализация бота
bot = Bot(TOKEN)

# Создание клавиатуры
main_keyboard = InlineKeyboard(
    [
        {"text": "Кнопка 1", "callback": "button1"},
    ],
    [ 
        {"text": "Кнопка 2", "callback": "button2"},
        {"text": "Кнопка 3", "callback": "button3"}
    ],
    [
        {"text": "Открыть ссылку", "url": "https://max.ru"}
    ]
)

# Обработчик события запуска бота
@bot.on("bot_started")
def on_start(ctx):
    ctx.reply(
        "Привет! Я бот с клавиатурой. Нажми на одну из кнопок ниже:",
        keyboard=main_keyboard
    )

# Обработчик команды '/keyboard'
@bot.command("keyboard")
def keyboard_command(ctx):
    ctx.reply(
        "Вот клавиатура. Выбери одну из опций:",
        keyboard=main_keyboard
    )

# Обработчик нажатий на кнопки
@bot.on("message_callback")
def handle_callback(ctx):
    logger = logging.getLogger(__name__)
    logger.info(f"Received callback with payload: {ctx.payload}")
    
    button = ctx.payload
    
    if button == "button1":
        ctx.reply_callback("Вы выбрали первую опцию")
    elif button == "button2":
        ctx.reply_callback("Вы выбрали вторую опцию")
    elif button == "button3":
        ctx.reply_callback("Вы выбрали третью опцию", 
                          keyboard=InlineKeyboard(
                              [{"text": "Вернуться к меню", "callback": "back_to_menu"}]
                          ))
    elif button == "back_to_menu":
        ctx.reply_callback("Вернемся к основному меню", keyboard=main_keyboard)
    else:
        ctx.reply_callback(f"Неизвестная кнопка: {button}")

# Запуск бота
if __name__ == "__main__":
    try:
        logger.info("Запуск бота...")
        bot.run()
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
        bot.stop()
        logger.info("Бот остановлен") 