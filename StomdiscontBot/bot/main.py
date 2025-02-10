from aiogram import Bot, Dispatcher
import asyncio


from Key import KEY
import logging
from handlers import router
from bot.DataBase.models import async_main

# Фулл запуск ниже





bot = Bot(token=KEY)
dp = Dispatcher()





async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)




async def stop_bot(): # Функция для корректной остановки
    await dp.stop_polling()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
    finally:
        stop_task = loop.create_task(stop_bot())
        loop.run_until_complete(stop_task)

