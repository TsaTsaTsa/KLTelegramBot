from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from core.config import ADMIN
from database.database import get_async_session
from handlers.admin.hello import admin_hello
from handlers.users.hello import user_hello
from models.users import users

router_h = Router()


@router_h.message(Command("start"))
async def hello_handler(msg: Message, state: FSMContext):
    async for session in get_async_session():
        async with session.begin():
            user_id = msg.chat.id
            result = await session.execute(select(users).where(users.c.user_id == user_id))
            result = result.fetchall()
            await session.commit()

            if str(user_id) == ADMIN:
                await admin_hello(msg, state, result)
            else:
                await user_hello(msg, state, result)
