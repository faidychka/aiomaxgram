"""
Python Max Bot API Client

Это библиотека для создания ботов для мессенджера Max
"""

from aiomaxgram.bot import Bot
from aiomaxgram.api import Api
from aiomaxgram.context import Context
from aiomaxgram.keyboards import InlineKeyboard

__version__ = "0.1.4"
__all__ = ["Bot", "Api", "Context", "InlineKeyboard"] 