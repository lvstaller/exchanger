import shelve
import asyncio

from aiogram.utils import executor

from user_bot.mics import dp, bot
import user_bot.handlers

DELAY = 20




async def update_price():
    print(await bot.get_me())


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop = loop)
