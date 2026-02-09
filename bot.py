import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = os.getenv("8576885534:AAGnTRAej4PTdVnsAzxWIYvXOPfLOQ5bKb4")
ADMIN_ID = int(os.getenv("825609212"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_mode = {}  

choice_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧑 З юзернеймом")],
        [KeyboardButton(text="👤 Анонімно")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привіт!\n"
        "Це бот зворотного звʼязку школи. Твої ідеї - ключ до розвитку нашого закладу:)\n\n"
        "Як ти хочеш надіслати ідею?",
        reply_markup=choice_keyboard
    )

@dp.message(lambda msg: msg.text in ["🧑 З юзернеймом", "👤 Анонімно"])
async def choose_mode(message: types.Message):
    if "Анонімно" in message.text:
        user_mode[message.from_user.id] = "anonymous"
        await message.answer(
            "👍 Добре. Напиши свою ідею:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        user_mode[message.from_user.id] = "username"
        await message.answer(
            "👍 Супер. Напиши свою ідею:",
            reply_markup=types.ReplyKeyboardRemove()
        )

@dp.message()
async def receive_feedback(message: types.Message):
    mode = user_mode.get(message.from_user.id)

    if not mode:
        await message.answer("Натисни /start 🙂")
        return

    if mode == "anonymous":
        text = f"📩 **АНОНІМНА ІДЕЯ**\n\n{message.text}"
    else:
        username = message.from_user.username or "без username"
        text = f"📩 **ІДЕЯ ВІД @{username}**\n\n{message.text}"

    await bot.send_message(ADMIN_ID, text)
    await message.answer("✅ Дякуємо! Твою ідею передано.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
