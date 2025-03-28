# API Reference

Библиотека Maxgram предоставляет простой интерфейс для работы с API Max. Ниже приведены основные классы и методы библиотеки.

## Класс Bot

Основной класс для создания бота.

```python
from maxgram import Bot

bot = Bot(token, client_options=None)
```

### Параметры

- `token` (str): Токен доступа бота, полученный от MasterBot
- `client_options` (Dict[str, Any], опционально): Настройки HTTP-клиента

### Методы

#### Декораторы для обработчиков

- `@bot.on(update_type)`: Регистрирует обработчик для указанного типа обновления
- `@bot.command(command_name)`: Регистрирует обработчик для команды (без слеша)
- `@bot.hears(pattern)`: Регистрирует обработчик для сообщений с определенным текстом

#### Управление ботом

- `bot.run(allowed_updates=None)`: Запускает получение обновлений через лонгполлинг
- `bot.stop()`: Останавливает получение обновлений
- `bot.catch(handler)`: Устанавливает пользовательский обработчик ошибок

## Класс Context

Контекст обработки обновления, доступный в обработчике.

### Свойства

- `update`: Полные данные обновления
- `update_type`: Тип обновления
- `chat_id`: Идентификатор чата (если есть)
- `user`: Информация о пользователе (если есть)
- `message`: Данные сообщения (если есть)
- `callback_id`: Идентификатор колбэка (если есть)
- `payload`: Полезные данные (если есть)

### Методы

- `reply(text, attachments=None)`: Отправляет ответ на текущее сообщение/обновление
- `answer_callback(text=None)`: Отправляет ответ на колбэк-запрос

## Класс Api

Класс для прямого взаимодействия с API Max.

```python
from maxgram import Api

api = Api(token, client_options=None)
```

### Методы

- `get_my_info()`: Получает информацию о текущем боте
- `set_my_commands(commands)`: Устанавливает команды для бота
- `send_message(chat_id, text, attachments=None)`: Отправляет сообщение в чат
- `answer_callback(callback_id, text=None)`: Отправляет ответ на колбэк
- `get_updates(allowed_updates, extra=None)`: Получает новые обновления от API

## Типы данных

### UpdateType

Константы для типов обновлений:

- `UpdateType.MESSAGE_CREATED`: Создание нового сообщения
- `UpdateType.MESSAGE_CALLBACK`: Нажатие на кнопку в сообщении
- `UpdateType.BOT_STARTED`: Запуск бота пользователем
- `UpdateType.MESSAGE_EDITED`: Редактирование сообщения
- `UpdateType.MESSAGE_DELETED`: Удаление сообщения
- `UpdateType.MESSAGE_CHAT_CREATED`: Создание чата через кнопку 