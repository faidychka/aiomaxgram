# Maxgram
v0.1.0 (28.03.2025)

Неофициальный Python клиент для [API MAX](https://dev.max.ru/)

Разработка в ранней стадии, поддерживается не все. Участие в развитии приветствуется!

Обсуждение в [MAX DevChat](https://max.ru/join/xzUCRiPjt_G7EaLtKLe7PgT69GPRP51BHHEv7n5W7J0) - неофициальный чат разработки ботов и приложений MAX

## Быстрый старт

### Установка
```sh
pip install maxgram
```

### Получение токена
Откройте диалог с [MasterBot](https://max.ru/masterbot), следуйте инструкциям и создайте нового бота. После создания бота MasterBot отправит вам токен.

### Пример пинг-понг эхо-бота
```python
from maxgram import Bot

# Инициализация бота
bot = Bot("BOT_TOKEN")

# Обработчик события запуска бота
@bot.on("bot_started")
def on_start(context):
    context.reply("Привет! Отправь мне ping, чтобы сыграть в пинг-понг или скажи /hello")

# Обработчик для сообщения с текстом 'ping'
@bot.hears("ping")
def ping_handler(context):
    context.reply("pong")

# Обработчик команды '/hello'
@bot.command("hello")
def hello_handler(context):
    context.reply("world")

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
```

### Обработка ошибок
Если во время обработки события произойдёт ошибка, Bot вызовет метод `bot.handle_error`. По умолчанию `bot.handle_error` просто выводит ошибку в консоль и продолжает работу, но вы можете переопределить это поведение, используя `bot.catch`.

> ⚠️ Завершайте работу программы при неизвестных ошибках, иначе бот может зависнуть в состоянии ошибки.

## Больше документаций и примеров

* [Документация](https://github.com/kayumovru/maxgram/tree/master/docs)

* [Примеры](https://github.com/kayumovru/maxgram/tree/master/examples)

## Для разработчиков

> В core/client.py смените уровень логирования с INFO до DEBUG

## Лицензия

MIT 