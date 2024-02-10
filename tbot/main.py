import asyncio
import logging
import sys, os
import qrcode
from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import Session
from datetime import date
from datetime import datetime as dt


from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, db_data
from models import Pupils, NewUsers

dp = Dispatcher()
engine = create_engine(db_data, echo=True)


kb = [
        [KeyboardButton(text="Показать qr-code")],
        [KeyboardButton(text="Отправить всем")],
    ]
gen_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_qr_code(hash):
    """ получение QR-кода"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
            )
    qr.add_data(hash)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"{hash}.png")
    return f"{hash}.png"

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    обработка команды /start
    """
    with Session(engine) as session:
        query = select(NewUsers.new_user_tg_id).where(NewUsers.new_user_tg_id == message.from_user.id)
        new_user = session.execute(query).fetchone()
        if not new_user:
            new_user = insert(NewUsers).values(new_user_name=message.from_user.full_name,
                                new_user_tg_id=message.from_user.id,
                                new_user_datetime=dt.now())
            session.execute(new_user)
            session.commit()
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}!", reply_markup=gen_kb)

@dp.message(F.text.lower() == 'показать qr-code')
async def command__handler_send_qr(message: Message) -> None:
    """
    Обработка  `Показать qr-code` command button
    """
    id = message.from_user.id
    with Session(engine) as session:
        query = select(Pupils).where(Pupils.tg_id == id)
        user = session.execute(query).first()
        if user:
            code = user[0].last_generated_code
            if code != 0:
                photo_name = get_qr_code(code)
                photo = FSInputFile(photo_name)
                dt = date.today().strftime("%d.%m.%Y")
                await message.answer_photo(photo, caption=f"Ваш код на {dt}")
                os.remove(photo_name)
            else:
                await message.answer(f"Вы уже вошли в школу, {hbold(message.from_user.full_name)}!", reply_markup=gen_kb)
    await command_start_handler("/start")

@dp.message(F.text.lower() == 'отправить всем')
async def command__handler_send_qr_all(message: Message) -> None:
    """
    Обраотка `Отправить всем` command button
    """
    with Session(engine) as session:
        # query = text(f"""SELECT tg_id, last_generated_code 
        #             FROM pupils WHERE tg_id!=0""")
        query = select(Pupils.tg_id, Pupils.last_generated_code).where(Pupils.tg_id != 0)
        users = session.execute(query).fetchall()
    for tg_id, last_generated_code in users:
        if last_generated_code != 0:
            photo = FSInputFile(get_qr_code(last_generated_code))
            await bot.send_photo(chat_id=tg_id, photo=photo)
            os.remove(photo)


async def main() -> None:
    """запуск бота"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    asyncio.run(main())