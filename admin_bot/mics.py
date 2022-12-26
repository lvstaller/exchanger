
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from databases import Base

import os
from config import token

bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())

engine = create_engine(f'sqlite:///base')

Base.metadata.create_all(engine)

if not os.path.isfile(f'./base'):
    Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)