#       ЭТОТ ФАЙЛ СОДЕРЖИТ ФУНКЦИИ ЗАПРОСОВ В БД

from bot.DataBase.models import async_session
from bot.DataBase.models import User, Category, Item, Basket
from sqlalchemy import select, insert, update

async def set_user(tg_id):              # ДОБАВЛЯЕТ НОВОГО ЮЗЕРА В ТАБЛИЦУ ЮЗЕР
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))


        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():             # ПОЛУЧАЕТ ВСЕ КАТЕГОРИИ ИЗ БД
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_item_category(category_id):           # ПОЛУЧАЕТ ВСЕ ТОВАРЫ У КОТОРЫХ Item.category == category_id (смотреть в файле models таблицы)
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Item).where(Item.category == category_id))
            items = result.scalars().all()
            return items


async def get_item(item_id):            # ПОЛУЧАЕТ ТОВАР ИЗ БД ПО ЕГО ID
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))

# async def get_amount_basket(basket_id: int):
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(select(Basket).where(Basket.id == basket_id))
#             items = result.scalars().all()
#             return items
#
# async def add_amount_basket(basket_id: int, amount_to_add: int, session: async_session):
#     """Добавляет amount_to_add к текущему количеству товаров в корзине."""
#     stmt = text(f"""UPDATE basket SET amount = amount + {amount_to_add} WHERE id = {basket_id}""")
#
#     await session.execute(stmt)
#     await session.commit()
#
#
# async def create_basket(basket_id: int, initial_amount: int = 0):
#     async with async_session() as session:
#         async with session.begin():
#
#             await session.execute(insert(Basket).values(id=basket_id, amount=initial_amount))
#             await session.commit()

async def create_basket(tg_id):             # СОЗДАЕТ КОРЗИНУ И ВПИСЫВАЕТ БАЗОВЫЕ НАСТРОЙКИ И ID ПОЛЬЗОВАТЕЛЯ
    async with async_session() as session:
        await session.execute(insert(Basket).values(id=tg_id, info='', amount='0.0'))
        await session.commit()

async def add_products_basket(tg_id, item_id):              # ДОБАВЛЯЕТ ПРОДУКТ В КОРЗИНУ (не работает вроде пока)
    async with async_session() as session:
        await session.execute(update(Basket).where(Basket.id == tg_id).values(info=item_id))
        await session.commit()




