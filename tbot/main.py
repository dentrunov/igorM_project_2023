import asyncio
import logging
import sys
import qrcode
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, db_data

dp = Dispatcher()
engine = create_engine(db_data, echo=True)


kb = [
        [KeyboardButton(text="Показать qr-code")],
        [KeyboardButton(text="Отправить всем")]
    ]
gen_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_qr_code(hash):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
            )
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{hash}.png")
    return f"{hash}.png"

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=gen_kb)

@dp.message(F.text.lower() == 'показать qr-code')
async def command__handler_send_qr(message: Message) -> None:
    """
    This handler receives messages with `Показать qr-code` command button
    """
    id = message.from_user.id
    with Session(engine) as session:
        query = text(f"""SELECT last_generated_code 
                    FROM pupils WHERE tg_id={id}""")
        user = session.execute(query).fetchall()
    photo = FSInputFile(get_qr_code(user[0][0]))
    await message.answer_photo(photo, caption="caption")
    

@dp.message(F.text.lower() == 'отправить всем')
async def command__handler_send_qr_all(message: Message) -> None:
    """
    This handler receives messages with `Отправить всемПоказать qr-code` command button
    """
    
    with Session(engine) as session:
        query = text(f"""SELECT tg_id, last_generated_code 
                    FROM pupils WHERE tg_id!=0""")
        users = session.execute(query).fetchall()
    for tg_id, last_generated_code in users:
        photo = FSInputFile(get_qr_code(last_generated_code))
        await bot.send_photo(chat_id=tg_id, photo=photo)

# @dp.message()
# async def test_all_handler(message: Message) -> None:
#     """
    
#     """
#     await message.answer(f"Hello, {hbold(message.from_user.ne)}!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    # bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)



logging.basicConfig(level=logging.INFO, stream=sys.stdout)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
asyncio.run(main())