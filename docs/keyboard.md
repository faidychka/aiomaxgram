# Использование клавиатуры

API Max позволяет добавлять интерактивные кнопки к сообщениям. Это позволяет создавать более удобные и интерактивные интерфейсы для общения с пользователями.

## Типы кнопок

В API Max доступны следующие типы кнопок:

- `callback`: Кнопка, при нажатии на которую бот получает событие `message_callback`
- `link`: Кнопка, открывающая ссылку в новой вкладке
- `request_contact`: Кнопка для запроса контактных данных пользователя
- `request_geo_location`: Кнопка для запроса местоположения пользователя
- `chat`: Кнопка для создания нового чата

## Создание клавиатуры

Чтобы добавить клавиатуру к сообщению, нужно создать вложение типа `inline_keyboard` и передать его в параметр `attachments` метода `reply` или `send_message`:

```python
from maxgram import Bot

bot = Bot("YOUR_BOT_TOKEN")

@bot.on("message_created")
def handle_message(ctx):
    # Создаем клавиатуру с одной кнопкой
    keyboard = {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {
                        "type": "callback",
                        "text": "Нажми меня",
                        "payload": "button_pressed"
                    }
                ]
            ]
        }
    }
    
    ctx.reply("Сообщение с кнопкой", attachments=[keyboard])
```

## Обработка нажатий на кнопки

Когда пользователь нажимает на кнопку типа `callback`, бот получает событие `message_callback`:

```python
@bot.on("message_callback")
def handle_callback(ctx):
    # Получаем payload из кнопки
    if ctx.payload == "button_pressed":
        ctx.answer_callback("Вы нажали кнопку!")
```

Метод `answer_callback` отправляет уведомление, которое будет показано пользователю.

## Примеры разных типов кнопок

### Кнопка с колбэком

```python
{
    "type": "callback",
    "text": "Нажми меня",
    "payload": "button_pressed"
}
```

### Кнопка со ссылкой

```python
{
    "type": "link",
    "text": "Открыть ссылку",
    "url": "https://example.com"
}
```

### Кнопка для создания чата

```python
{
    "type": "chat",
    "text": "Обсудить",
    "chat_title": "Обсуждение сообщения"
}
```

## Расположение кнопок

Кнопки в клавиатуре располагаются в виде двумерного массива, где:
- Внешний массив представляет строки
- Внутренний массив представляет кнопки в строке

Например, для создания клавиатуры с двумя строками, где в первой строке одна кнопка, а во второй - две:

```python
keyboard = {
    "type": "inline_keyboard",
    "payload": {
        "buttons": [
            [  # Первая строка
                {"type": "callback", "text": "Кнопка 1", "payload": "button1"}
            ],
            [  # Вторая строка
                {"type": "callback", "text": "Кнопка 2", "payload": "button2"},
                {"type": "callback", "text": "Кнопка 3", "payload": "button3"}
            ]
        ]
    }
} 