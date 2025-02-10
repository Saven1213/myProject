from unittest.mock import DEFAULT

from aiogram.client.default import Default
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


#                           Настройка SQLalchemy
# ________________________________________________________________________
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

#__________________________________________________________________________

#                                       СОЗДАНИЕ ТАБЛИЦ (я думаю разберешься)
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(Integer)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(120))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))


class Basket(Base):
    __tablename__ = 'basket'

    id: Mapped[int] = mapped_column(primary_key=True)
    info: Mapped[str] = mapped_column(String(125))
    amount: Mapped[float] = mapped_column()




async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

