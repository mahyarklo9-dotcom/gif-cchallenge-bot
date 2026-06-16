from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import os
import random

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

games = {}

SCENARIOS = [
"اشتباهی پیام عاشقانه برای رئیست فرستادی!",
"وسط عروسی زمین خوردی!",
"وقتی فهمیدی فردا امتحان داری!",
"دوستت رمز وای‌فای را عوض کرده!",
"وقتی شارژ گوشی ۱٪ است!",
"وقتی به جای معلم به گروه کلاس میم فرستادی!",
"وقتی مامان میگه بیا کارت دارم!",
"وقتی فهمیدی غذای مورد علاقه‌ات تموم شده!",
"وقتی ساعت را نگاه می‌کنی و برای کار دیر کردی!",
"وقتی دوستت میگه یه سوال کوچیک دارم!"
]

def get_chat(chat_id):
if chat_id not in games:
games[chat_id] = {
"started": False,
"players": {},
"round": 0,
"submitted": set()
}
return games[chat_id]

@dp.message(Command("start"))
async def start(message: Message):
await message.answer("🎉 ربات فعال است!")

@dp.message(Command("newgame"))
async def new_game(message: Message):
chat = get_chat(message.chat.id)

chat["started"] = False
chat["players"] = {}
chat["round"] = 0
chat["submitted"] = set()

await message.answer(
    "🎮 بازی جدید ساخته شد!\n\n"
    "برای ورود:\n"
    "/join"
)

@dp.message(Command("join"))
async def join_game(message: Message):
chat = get_chat(message.chat.id)

if chat["started"]:
    await message.answer("بازی شروع شده است.")
    return

user_id = message.from_user.id

chat["players"][user_id] = {
    "name": message.from_user.first_name
}

await message.answer(
    f"✅ {message.from_user.first_name} وارد بازی شد."
)

@dp.message(Command("players"))
async def players(message: Message):
chat = get_chat(message.chat.id)

if not chat["players"]:
    await message.answer("هنوز کسی وارد نشده.")
    return

text = "👥 بازیکنان:\n\n"

for p in chat["players"].values():
    text += f"• {p['name']}\n"

await message.answer(text)

@dp.message(Command("startgame"))
async def start_game(message: Message):
chat = get_chat(message.chat.id)

if len(chat["players"]) < 2:
    await message.answer(
        "❌ حداقل ۲ بازیکن لازم است."
    )
    return

chat["started"] = True
chat["round"] = 1
chat["submitted"] = set()

scenario = random.choice(SCENARIOS)

await message.answer(
    f"🎯 راند ۱\n\n{scenario}\n\n"
    "همه یک GIF ارسال کنند."
)

@dp.message(F.animation)
async def gif_received(message: Message):
chat = get_chat(message.chat.id)

if not chat["started"]:
    return

user_id = message.from_user.id

if user_id not in chat["players"]:
    return

if user_id in chat["submitted"]:
    await message.reply(
        "⛔ GIF این راند را قبلاً فرستادی."
    )
    return

chat["submitted"].add(user_id)

remain = (
    len(chat["players"])
    - len(chat["submitted"])
)

await message.reply(
    f"✅ ثبت شد.\n"
    f"{remain} نفر باقی مانده."
)

if len(chat["submitted"]) == len(chat["players"]):

    chat["round"] += 1
    chat["submitted"] = set()

    scenario = random.choice(SCENARIOS)

    await message.answer(
        f"🎯 راند {chat['round']}\n\n"
        f"{scenario}\n\n"
        "GIF بعدی را ارسال کنید."
    )

async def main():
print("Bot Started...")
await dp.start_polling(bot)

if name == "main":
asyncio.run(main())
