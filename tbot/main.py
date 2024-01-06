import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from config import TOKEN

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message(Command(commands='set'))
async def command__handler(message: Message) -> None:
    """
    This handler receives messages with `/set` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message(F.text == 'список')
async def test_handler(message: Message) -> None:
    """
    This handler receives messages with `список` text
    """
    await message.answer("Hello!")

@dp.message()
async def test_all_handler(message: Message) -> None:
    """
    
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())