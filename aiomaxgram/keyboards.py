"""
Модуль для работы с клавиатурами в Max API
"""

from typing import List, Dict, Any, Union, Optional


class InlineKeyboard:
    """
    Класс для удобного создания inline-клавиатур в Max

    Пример использования:
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
    """

    def __init__(self, *rows: List[Dict[str, str]]):
        """
        Создает inline-клавиатуру из строк кнопок

        Args:
            *rows: Списки словарей, описывающих кнопки в каждой строке
                  Каждая кнопка может содержать следующие параметры:
                  - text: Текст кнопки
                  - callback: Данные обратного вызова (тип кнопки будет callback)
                  - url: URL для кнопки с ссылкой (тип кнопки будет link)
                  - chat_title: Название чата для создания (тип кнопки будет chat)
                  - chat_description: Описание чата (опционально, для типа chat)
        """
        self.rows = rows
        
    def to_attachment(self) -> Dict[str, Any]:
        """
        Преобразует клавиатуру в формат вложения для отправки API

        Returns:
            Словарь с параметрами клавиатуры для отправки в API
        """
        buttons = []
        
        for row in self.rows:
            button_row = []
            
            for button in row:
                btn_data = {"text": button["text"]}
                
                if "callback" in button:
                    btn_data["type"] = "callback"
                    btn_data["payload"] = button["callback"]
                elif "url" in button:
                    btn_data["type"] = "link"
                    btn_data["url"] = button["url"]
                elif "chat_title" in button:
                    btn_data["type"] = "chat"
                    btn_data["chat_title"] = button["chat_title"]
                    if "chat_description" in button:
                        btn_data["chat_description"] = button["chat_description"]
                # Дополнительные типы кнопок можно добавить здесь
                
                button_row.append(btn_data)
            
            if button_row:
                buttons.append(button_row)
        
        return {
            "type": "inline_keyboard",
            "payload": {
                "buttons": buttons
            }
        } 