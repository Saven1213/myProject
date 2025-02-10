from pickletools import markobject
from venv import create

from aiofiles.os import replace
from pyexpat.errors import messages
from sqlalchemy.util import await_fallback

import bot.DataBase.requests as rq
from aiogram import F, Router, Bot, types #                 Импорт роутера и F
from aiogram.filters import CommandStart, Command, StateFilter  #    Импорт команды CommandStart и Command
from aiogram.types import Message, CallbackQuery, Dice       #       Импорт типа Massage и callback
from aiogram.fsm.state import StatesGroup, State
import Keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from bot.DataBase.requests import create_basket, add_products_basket

router = Router()


@router.message(CommandStart())
async def StartButton(message:Message):
    id_us = message.from_user.id
    await rq.set_user(id_us)
    await message.answer("""Stomdiscont\n
    Стоматологические товары по низким ценам
    """, reply_markup=kb.main)
    await create_basket(id_us)


@router.message(F.text == 'Каталог')
async def Catalog_button(message:Message):
    await message.answer("Выберите категорию товара", reply_markup=await kb.categories())
# @router.callback_query(F.data == 'make_order')
# async def Make_order(callback:CallbackQuery):
#     await callback.message.edit_text('добавьте товар в корзину', kb.order_size)

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    try:
        category_id = callback.data.split('_')[1]
        await callback.answer('вы выбрали категорию')
        await callback.message.answer('Выберите товар по категории', reply_markup=await kb.items(category_id))
    except Exception as e:
        await callback.answer(f"Ошибка: {e}") # Добавлено для выявления ошибок
        print(f"Exception in category handler: {e}")
@router.callback_query(F.data == 'back')
async def to_back_page(callback:CallbackQuery):
    await callback.message.edit_text('Выберите категорию товара', reply_markup=await kb.categories())

@router.callback_query(F.data == 'to_main')
async def to_main_page(callback:CallbackQuery):
    await callback.message.answer("""Stomdiscont\n
    Стоматологические товары по низким ценам
    """, reply_markup=kb.main)


@router.callback_query(F.data.startswith('item_'))
async def category(callback: CallbackQuery):
    item_id = callback.data.split('_')[1]
    item_data = await rq.get_item(item_id)
    await callback.answer('Вы выбрали товар')
    await callback.message.edit_text(
        f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}р', reply_markup=kb.add_to_basket)
    info = callback.message.from_user.id
    await add_products_basket(info, item_data.id)       # Тупанул, эта функция должна быть в хендлере ниже, но я хз как найти в итоге нужный item_data


@router.callback_query(F.data == 'add_basket')
async def add_basket_b(callback:CallbackQuery):
    await callback.answer('Товар в корзине!')
    await callback.message.edit_text('Выберите категорию товара', reply_markup=kb.main)






















# @router.callback_query(F.data == '-')
# async def minus(callback:CallbackQuery):
#     if amount_result == 0:
#         pass
#     elif amount_result > 0:
#         amount_result -= 1
#     await callback.message.edit_text('')