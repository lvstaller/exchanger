from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import os
from .config import token
from .language_configuration import LanguageConfiguration

bot = Bot(token, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())

locale_configurator = LanguageConfiguration("user_bot/locale.json")
