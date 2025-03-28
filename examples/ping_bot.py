"""
Простой пинг-понг бот для Max

Этот бот отвечает на команду /ping сообщением "pong"
и повторяет все остальные сообщения.
"""

from maxgram import Bot

# Инициализация бота
# Внимание! Рекомендуется через .env получать токен!
bot = Bot("YOUR_BOT_TOKEN")

# Установка подсказок для команд бота
bot.set_my_commands({
    "help": "Получить помощь",
    "hello": "Приветствие"
})

# Обработчик события запуска бота
@bot.on("bot_started")
def on_start(context):
    context.reply("Привет! Отправь мне ping, чтобы сыграть в пинг-понг или выбери /hello")

# Обработчик для сообщения с текстом 'ping'
@bot.hears("ping")
def ping_handler(context):
    context.reply("pong")

# Обработчик команды '/hello'
@bot.command("hello")
def hello_handler(context):
    context.reply("world")

# Обработчик команды '/help'
@bot.command("help")
def help_handler(context):
    commands_info = """
Доступные команды:
/help - Получить список команд
/hello - Получить приветствие
    """
    context.reply(commands_info)

# Обработчик для всех остальных входящих сообщений
@bot.on("message_created")
def echo(context):
    # Проверяем, что есть сообщение и тело сообщения
    if context.message and context.message.get("body") and "text" in context.message["body"]:
        # Получаем текст сообщения
        text = context.message["body"]["text"]
        
        # Проверяем, что это не команда и не специальные сообщения с обработчиками
        if not text.startswith("/") and text != "ping" and text != "hello":
            context.reply(text)

# Запуск бота
if __name__ == "__main__":
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.stop()