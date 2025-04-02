"""
Python Max Bot API Client

Это библиотека для создания ботов для мессенджера Max
"""

from aioaiomaxgram.bot import Bot
from aioaiomaxgram.api import Api
from aioaiomaxgram.context import Context
from aioaiomaxgram.keyboards import InlineKeyboard

__version__ = "0.1.4"
__all__ = ["Bot", "Api", "Context", "InlineKeyboard"] 