"""
Контекст для обработки обновлений
"""

from typing import Dict, Any, Optional, List, Union
import logging

from maxgram.types import Update, Message, UpdateType


class Context:
    """
    Контекст для обработки обновлений
    
    Содержит информацию о текущем обновлении и методы для работы с ним
    """
    
    def __init__(self, update: Dict[str, Any], api):
        """
        Инициализация контекста
        
        Args:
            update: Данные обновления
            api: API-клиент
        """
        self.update = update
        self.api = api
        
        # Логируем структуру обновления для диагностики
        logging.getLogger(__name__).debug(f"Context init with update: {update}")
        
        # Устанавливаем свойства в зависимости от типа обновления
        self.update_type = update.get('update_type')
        self.chat_id = update.get('chat_id')
        self.user = update.get('user')
        self.message = update.get('message')
        self.callback_id = update.get('callback_id')
        self.payload = update.get('payload')
        
        # Если callback_id не указан в корне обновления, но это callback-обновление
        if not self.callback_id and self.update_type == 'message_callback' and 'callback' in update:
            # Извлекаем callback_id из вложенной структуры
            self.callback_id = update['callback'].get('callback_id')
            # Если payload не задан, но есть в callback
            if not self.payload and 'payload' in update['callback']:
                self.payload = update['callback'].get('payload')
        
        # Если chat_id не указан в корне обновления
        if not self.chat_id:
            # Попробуем получить из message -> recipient -> chat_id
            if self.message and 'recipient' in self.message and 'chat_id' in self.message['recipient']:
                self.chat_id = self.message['recipient']['chat_id']
            # Для обратной совместимости проверяем и прямое указание chat_id в сообщении
            elif self.message and 'chat_id' in self.message:
                self.chat_id = self.message.get('chat_id')
    
    def reply(self, text: str, attachments: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Отправляет ответ на текущее сообщение/обновление
        
        Args:
            text: Текст сообщения
            attachments: Вложения сообщения
            
        Returns:
            Информация об отправленном сообщении
        """
        chat_id = self._get_chat_id()
        if not chat_id:
            raise ValueError("Cannot reply without chat_id in context")
        
        return self.api.send_message(
            chat_id,
            text,
            attachments
        )
    
    def _get_chat_id(self) -> Optional[int]:
        """
        Получает идентификатор чата из контекста обновления
        
        Returns:
            Идентификатор чата или None если его нет
        """
        # Сначала пробуем использовать сохраненный chat_id
        if self.chat_id:
            return self.chat_id
            
        # Пробуем получить из message -> recipient -> chat_id
        if self.message:
            if 'recipient' in self.message and 'chat_id' in self.message['recipient']:
                return self.message['recipient']['chat_id']
            elif 'chat_id' in self.message:
                return self.message['chat_id']
                
        return None
    
    def answer_callback(self, text: Optional[str] = None) -> Dict[str, Any]:
        """
        Отправляет ответ на колбэк-запрос
        
        Args:
            text: Текст уведомления
            
        Returns:
            Результат операции
        """
        if not self.callback_id:
            raise ValueError("Cannot answer callback without callback_id in context")
            
        return self.api.answer_callback(
            self.callback_id,
            text
        ) 