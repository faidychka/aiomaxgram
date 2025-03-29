# Адаптация клавиатур в maxgram для упрощения работы с API Max

Документация по адаптации и улучшению работы с клавиатурами в библиотеке maxgram.

## Описание проблемы

Исходный API Max требует создания вложений с клавиатурами в формате JSON, что не очень удобно для разработчиков:

```json
{
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
```

Использование такого формата в Python-коде требует написания нестандартных словарей с множеством вложенных структур, что усложняет код и увеличивает вероятность ошибок.

Также, процесс обработки нажатий на кнопки требовал вызова двух отдельных методов: `answer_callback` для ответа на колбэк и `reply` для отправки нового сообщения.

## Решение

Мы разработали интуитивно понятный API для работы с клавиатурами:

1. Создали класс `InlineKeyboard` в модуле `maxgram.keyboards`
2. Реализовали метод `reply_callback` в классе `Context` для объединения двух операций в одну
3. Добавили параметр `keyboard` в метод `reply` для упрощения отправки клавиатур

## Улучшения в деталях

### 1. Класс InlineKeyboard

Класс `InlineKeyboard` позволяет создавать клавиатуры с простым и интуитивным интерфейсом:

```python
keyboard = InlineKeyboard(
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
```

Где:
- Каждый аргумент функции-конструктора представляет собой строку кнопок
- Каждая строка - это список кнопок в виде словарей
- Каждая кнопка описывается простым словарем с понятными ключами:
  - `text`: Текст кнопки
  - `callback`: Данные для кнопок типа callback
  - `url`: URL для кнопок с ссылками
  - `chat_title`: Название чата для кнопок создания чата

Внутри класс преобразует эту простую структуру в сложный формат, требуемый API Max.

### 2. Метод reply с поддержкой клавиатур

Добавлен параметр `keyboard` в метод `reply` класса `Context`:

```python
def reply(self, text: str, attachments: Optional[List[Dict[str, Any]]] = None, keyboard: Optional[Any] = None)
```

Этот параметр может принимать:
- Объект `InlineKeyboard`
- Словарь с данными клавиатуры в формате API Max (для обратной совместимости)

Метод автоматически обнаруживает тип объекта и добавляет его во вложения сообщения.

### 3. Метод reply_callback для одновременной обработки колбэков

Для упрощения обработки нажатий на кнопки добавлен метод `reply_callback`:

```python
def reply_callback(self, text: str, attachments: Optional[List[Dict[str, Any]]] = None, 
                  keyboard: Optional[Any] = None, notification: Optional[str] = None)
```

Этот метод автоматически:
1. Отправляет ответ на колбэк через `answer_callback`
2. Отправляет новое сообщение через `reply`

Если текст уведомления для колбэка не указан, он генерируется автоматически на основе payload и текущего времени.

## Примеры использования

### Создание клавиатуры

```python
from maxgram.keyboards import InlineKeyboard

main_keyboard = InlineKeyboard(
    [{"text": "Кнопка 1", "callback": "button1"}],
    [{"text": "Кнопка 2", "callback": "button2"}, {"text": "Кнопка 3", "callback": "button3"}],
    [{"text": "Открыть ссылку", "url": "https://max.ru"}]
)
```

### Отправка сообщения с клавиатурой

```python
@bot.command("keyboard")
def keyboard_command(ctx):
    ctx.reply(
        "Выберите опцию:",
        keyboard=main_keyboard
    )
```

### Обработка нажатий на кнопки

```python
@bot.on("message_callback")
def handle_callback(ctx):
    button = ctx.payload
    
    if button == "button1":
        ctx.reply_callback("Вы выбрали первую опцию")
    elif button == "button2":
        ctx.reply_callback("Вы выбрали вторую опцию", keyboard=another_keyboard)
```

## Миграция с предыдущего API

Старый способ работы с клавиатурами все еще поддерживается для обратной совместимости:

```python
# Старый способ (работает)
keyboard = {
    "type": "inline_keyboard",
    "payload": {
        "buttons": [[{"type": "callback", "text": "Кнопка", "payload": "data"}]]
    }
}
ctx.reply("Сообщение", attachments=[keyboard])

# Новый способ
keyboard = InlineKeyboard([{"text": "Кнопка", "callback": "data"}])
ctx.reply("Сообщение", keyboard=keyboard)
```

Обработка колбэков также поддерживает оба варианта:

```python
# Старый способ (работает)
ctx.answer_callback("Уведомление")
ctx.reply("Ответное сообщение")

# Новый способ
ctx.reply_callback("Ответное сообщение", notification="Уведомление")
``` 