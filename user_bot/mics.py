
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from databases import Base

import os
from config import token
from user_bot.language_configuration import LanguageConfiguration

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

locale_configurator = LanguageConfiguration("locale.json")