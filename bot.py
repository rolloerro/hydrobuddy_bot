import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(types.KeyboardButton(text="💧 Выпил воду"))
    kb.add(types.KeyboardButton(text="📊 Статистика"))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "💧 *HydroBuddy*\n\nЯ помогу тебе пить воду регулярно.\nНажимай кнопку каждый раз, когда выпил стакан 👇",
        reply_markup=keyboard(),
        parse_mode="Markdown"
    )

@dp.message(lambda m: m.text == "💧 Выпил воду")
async def drink(message: types.Message):
    data = load_data()
    uid = str(message.from_user.id)
    data[uid] = data.get(uid, 0) + 1
    save_data(data)
    await message.answer(f"🔥 Отлично! Сегодня уже *{data[uid]}* стаканов 💧", parse_mode="Markdown")

@dp.message(lambda m: m.text == "📊 Статистика")
async def stats(message: types.Message):
    data = load_data()
    count = data.get(str(message.from_user.id), 0)
    await message.answer(f"📊 Сегодня ты выпил *{count}* стаканов воды 💧", parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
