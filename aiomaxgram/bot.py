"""
Класс бота для работы с API Max
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable, Union, Type, Awaitable
import functools
import re
import json

from aiomaxgram.api import Api
from aiomaxgram.context import Context
from aiomaxgram.types import UpdateType
from aiomaxgram.core.network.polling import Polling

logger = logging.getLogger(__name__)

# Типы обработчиков
# Change handler type to support async functions
HandlerFunc = Callable[[Context], Awaitable[None]]


class Bot:
    """
    Основной класс для работы с ботом
    
    Предоставляет методы для обработки обновлений и отправки ответов
    """
    
    def __init__(self, token: str, client_options: Optional[Dict[str, Any]] = None):
        """
        Инициализация бота
        
        Args:
            token: Токен доступа бота
            client_options: Дополнительные настройки клиента
        """
        self.api = Api(token, client_options)
        self.handlers = {
            "update": [],  # Общие обработчики для всех типов обновлений
            UpdateType.MESSAGE_CREATED: [],
            UpdateType.MESSAGE_CALLBACK: [],
            UpdateType.BOT_STARTED: [],
            UpdateType.MESSAGE_EDITED: [],
            UpdateType.MESSAGE_DELETED: [],
            UpdateType.MESSAGE_CHAT_CREATED: [],
        }
        self.command_handlers = {}  # Обработчики команд: {"command": [handler1, handler2, ...]}
        self.text_handlers = []  # Обработчики текста: [(pattern, handler), ...]
        
        self.polling = None
        self.is_running = False
    
    def on(self, update_type: str):
        """
        Декоратор для регистрации обработчика определенного типа обновлений
        
        Args:
            update_type: Тип обновления (см. UpdateType)
        """
        def decorator(func: HandlerFunc):
            self.handlers.setdefault(update_type, []).append(func)
            return func
        return decorator
    
    def command(self, command_name: str):
        """
        Декоратор для регистрации обработчика команды
        
        Args:
            command_name: Имя команды (без слеша)
        """
        def decorator(func: HandlerFunc):
            self.command_handlers.setdefault(command_name, []).append(func)
            return func
        return decorator
    
    def hears(self, pattern: str):
        """
        Декоратор для регистрации обработчика текстовых сообщений по шаблону
        
        Args:
            pattern: Шаблон текста (точное совпадение или регулярное выражение)
        """
        def decorator(func: HandlerFunc):
            self.text_handlers.append((pattern, func))
            return func
        return decorator
    
    async def start(self, allowed_updates: Optional[List[str]] = None):
        """
        Запускает получение обновлений
        
        Args:
            allowed_updates: Список типов обновлений, которые нужно получать
        """
        if self.is_running:
            logger.warning("Bot is already running")
            return
        
        self.is_running = True
        
        self.polling = Polling(self.api, allowed_updates)
        
        await self.polling.loop(self._process_update)

    def run(self, allowed_updates: Optional[List[str]] = None):
        """Обертка для запуска корутины"""
        asyncio.run(self.start(allowed_updates))
    
    def stop(self):
        """Останавливает получение обновлений"""
        if not self.is_running:
            logger.warning("Bot is not running")
            return
        
        if self.polling:
            self.polling.stop()
        
        self.is_running = False
    
    async def _process_update(self, update: Dict[str, Any]):
        """
        Обрабатывает входящее обновление
        
        Args:
            update: Данные обновления
        """
        try:
            logger.debug(f"Received update: {json.dumps(update, ensure_ascii=False)}")
            
            update_type = update.get("update_type")
            context = Context(update, self.api)
            
            # Вызываем общие обработчики
            for handler in self.handlers.get("update", []):
                await handler(context)
            
            # Вызываем обработчики для конкретного типа обновления
            for handler in self.handlers.get(update_type, []):
                await handler(context)
            
            # Обрабатываем сообщения особым образом
            if update_type == UpdateType.MESSAGE_CREATED and "message" in update:
                await self._process_message(context)
                
        except Exception as e:
            await self.handle_error(e, update)

    async def _process_message(self, context: Context):
        """
        Обрабатывает входящее сообщение
        
        Args:
            context: Контекст обновления
        """
        if not context.message:
            return
            
        message_body = context.message.get("body", {})
        if not message_body or "text" not in message_body:
            return
            
        text = message_body["text"]
        
        if text.startswith("/"):
            command_parts = text[1:].split(" ", 1)
            command = command_parts[0].lower()
            
            logger.debug(f"Received command: /{command}")
            
            handlers = self.command_handlers.get(command, [])
            if handlers:
                for handler in handlers:
                    await handler(context)
            else:
                logger.debug(f"No handler found for command: /{command}")
                
        # Проверяем обработчики текста
        for pattern, handler in self.text_handlers:
            if pattern == text or re.search(pattern, text):
                await handler(context)

    async def handle_error(self, error: Exception, update: Dict[str, Any]):
        """
        Обрабатывает ошибку при обработке обновления
        
        Args:
            error: Ошибка
            update: Данные обновления
        """
        logger.error(f"Error while processing update: {error}", exc_info=True)

    def catch(self, handler: Callable[[Exception, Dict[str, Any]], Awaitable[None]]):
        """
        Устанавливает пользовательский обработчик ошибок
        
        Args:
            handler: Функция-обработчик ошибок
        """
        self.handle_error = handler
        return self

    async def set_my_commands(self, commands: Dict[str, str]) -> Dict[str, Any]:
        """
        Устанавливает команды для бота в удобном формате
        
        Args:
            commands: Словарь команд в формате {"command": "description"}
            
        Returns:
            Результат запроса PATCH /me
        """
        commands_list = [{"name": name, "description": description} 
                        for name, description in commands.items()]
        return await self.api.set_my_commands(commands_list)