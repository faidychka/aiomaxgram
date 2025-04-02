"""
Базовый HTTP-клиент для API Max
"""

import aiohttp
from typing import Dict, Any, Optional, Union, List
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Client:
    """Класс для выполнения HTTP-запросов к API Max"""
    
    BASE_URL = "https://botapi.max.ru"
    
    def __init__(self, token: str, client_options: Optional[Dict[str, Any]] = None):
        """
        Инициализация клиента
        
        Args:
            token: Токен доступа бота
            client_options: Дополнительные настройки клиента
        """
        self.token = token
        self.options = client_options or {}
        self.session = None
    
    def _build_url(self, path: str) -> str:
        """
        Формирует полный URL для запроса
        
        Args:
            path: Путь к методу API
            
        Returns:
            Полный URL для запроса
        """
        url = f"{self.BASE_URL}{path}"
        if "?" in url:
            url += f"&access_token={self.token}"
        else:
            url += f"?access_token={self.token}"
        return url
    
    async def request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None, 
                data: Optional[Dict[str, Any]] = None, files: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполняет запрос к API
        
        Args:
            method: HTTP-метод (GET, POST, PUT, DELETE)
            path: Путь к методу API
            params: Параметры запроса
            data: Данные для отправки в теле запроса
            files: Файлы для отправки
            
        Returns:
            Ответ от API в виде словаря
            
        Raises:
            Exception: При ошибке запроса
        """
        url = self._build_url(path)
        
        headers = {
            "User-Agent": f"aiomaxgramPython/0.1.0",
        }
        
        # Подготовка данных для JSON
        json_data = None
        if data and not files:
            headers["Content-Type"] = "application/json"
            json_data = data
        
        logger.debug(f"Request: {method} {url}")
        if params:
            logger.debug(f"Params: {params}")
        if data:
            logger.debug(f"Data: {data}")
        
        # Создаем сессию, если она еще не создана
        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.options.get("timeout", 60))
            
            async with self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                data=None if json_data else data,
                headers=headers,
                timeout=timeout
            ) as response:
                # Проверка статуса ответа
                if response.status >= 400:
                    error_text = f"HTTP error: {response.status} {response.reason}"
                    try:
                        error_json = await response.json()
                        error_text = f"{error_text}, API response: {error_json}"
                    except:
                        error_text = f"{error_text}, Response text: {await response.text()}"
                    
                    logger.error(error_text)
                    raise Exception(error_text)
                
                result = await response.json()
                logger.debug(f"Response: {result}")
                return result
                
        except aiohttp.ClientError as e:
            error_text = f"Request error: {e}"
            logger.error(error_text)
            raise Exception(error_text)
        except Exception as e:
            logger.error(f"Request error: {e}")
            raise