from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


import os
from config import token

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())
