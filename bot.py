from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
import os
import random

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN is not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

games = {}

# =========================
# 🎯 SCENARIOS (FULL LIST)
# =========================
SCENARIOS = [
"وقتی ساعت ۳ صبح یادت می‌افتد فردا امتحان داری!",
"وقتی شارژ گوشی به ۱٪ رسیده!",
"وقتی اشتباهی پیام را برای رئیست فرستادی!",
"وقتی مادرت می‌گوید مهمان داریم!",
"وقتی اینترنت وسط بازی قطع می‌شود!",
"وقتی دوستت می‌گوید فقط یک سوال کوچیک دارم!",
"وقتی رمز کارت یادت نمی‌آید!",
"وقتی متوجه می‌شوی امروز تعطیل نیست!",
"وقتی غذا را سفارش دادی و اشتباه آوردند!",
"وقتی از خواب بیدار می‌شوی و فکر می‌کنی دیر شده!",
"وقتی با اعتماد به نفس وارد اتاق می‌شوی و می‌فهمی اتاق اشتباه بوده!",
"وقتی جلوی آینه ژست می‌گیری و کسی پشت سرت می‌خندد!",
"وقتی با عجله می‌دوی ولی می‌بینی در بسته بوده!",
"وقتی می‌خواهی اسم کسی را صدا بزنی و یادت نمی‌آید!",
"وقتی می‌گویی «من دارم می‌رم» و تازه لباس نپوشیدی!",
"وقتی با صدای بلند آهنگ می‌خوانی و می‌فهمی هدفونت وصل نبوده!",
"وقتی روی صندلی می‌نشینی و می‌فهمی از قبل خیس بوده!",
"وقتی می‌خواهی خیلی شیک حرف بزنی ولی زبانت می‌گیرد!",
"وقتی به سطل زباله می‌زنی ولی توپ نیست، مچاله کاغذه!",
"وقتی داری از پله‌ها پایین می‌آیی و یک پله کم می‌آوری!",
"وقتی پیام «الان میام» را فرستادی و هنوز از تخت بلند نشدی!",
"وقتی برای کسی دست تکان می‌دهی و می‌فهمی با تو نبوده!",
"وقتی در آسانسور فقط تویی و یک نفر دیگر و هر دو به دیوار نگاه می‌کنید!",
"وقتی می‌خواهی خونسرد باشی ولی لیوان از دستت لیز می‌خورد!",
"وقتی فکر می‌کنی میکروفون خاموشه ولی روشن بوده!",
"وقتی وسط صحبت یادت می‌رود داشتی چی می‌گفتی!",
"وقتی گوشی رو دستته ولی دنبالش می‌گردی!",
"وقتی فکر می‌کنی کسی نگات می‌کنه و واقعاً داره نگات می‌کنه!",
"وقتی می‌خوای خفن باشی ولی زمین می‌خوری!",
"وقتی پیام رو اشتباهی برای گروه می‌فرستی!",
"وقتی وسط خنده سرفه می‌کنی!",
"وقتی می‌خوای سریع جواب بدی ولی اینترنت هنگ می‌کنه!",
"وقتی فکر می‌کنی زنگ خورد ولی تو ذهنت بوده!",
"وقتی در بسته‌ست ولی هلش می‌دی!",
"وقتی می‌خوای آروم در رو ببندی ولی صداش کل خونه رو می‌لرزونه!",
"وقتی فکر می‌کنی فیلمو دیدی ولی آخرش یادت نیست!",
"وقتی می‌خوای حرفه‌ای تایپ کنی ولی کیبورد قاطی می‌کنه!",
"وقتی می‌خوای از در رد شی ولی شیشه‌ایه!",
"وقتی فکر می‌کنی وای‌فای قطعه ولی رمز اشتباهه!",
"وقتی یه جوک می‌گی و خودت بیشتر می‌خندی!",
"وقتی می‌خوای پیامو ادیت کنی ولی پاکش می‌کنی!",
"وقتی می‌خوای جدی باشی ولی خنده می‌گیره!"
]

# =========================
# 🎮 GAME DATA
# =========================
def get_game(chat_id):
    if chat_id not in games:
        games[chat_id] = {
            "started": False,
            "players": {},
            "round": 0,
            "submitted": set(),
            "scores": {},
            "gifs": {},
            "used_scenarios": [],
            "votes": {}
        }
    return games[chat_id]

# =========================
# 🚀 INFO COMMAND (NEW)
# =========================
@dp.message(Command("info"))
async def info(message: Message):
    await message.answer("🛠 ساخته شده توسط @Jack_landon")

# =========================
# 🚀 START
# =========================
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("🎮 GIF Challenge Bot فعال است!\n\n/newgame")

# =========================
# 🆕 NEW GAME
# =========================
@dp.message(Command("newgame"))
async def newgame(message: Message):
    games[message.chat.id] = {
        "started": False,
        "players": {},
        "round": 0,
        "submitted": set(),
        "scores": {},
        "gifs": {},
        "used_scenarios": [],
        "votes": {}
    }

    await message.answer("🎮 بازی جدید ساخته شد!\n\n/join")

# =========================
# 👤 JOIN
# =========================
@dp.message(Command("join"))
async def join(message: Message):
    game = get_game(message.chat.id)

    if game["started"]:
        return await message.answer("⚠️ بازی شروع شده")

    uid = message.from_user.id

    if uid in game["players"]:
        return await message.answer("⚠️ قبلاً وارد شدی")

    game["players"][uid] = message.from_user.first_name
    game["scores"][uid] = 0

    await message.answer(f"✅ {message.from_user.first_name} وارد شد")

# =========================
# 🚀 START GAME
# =========================
@dp.message(Command("startgame"))
async def startgame(message: Message):
    game = get_game(message.chat.id)

    if len(game["players"]) < 2:
        return await message.answer("❌ حداقل ۲ نفر لازم است")

    game["started"] = True
    game["round"] = 1
    game["submitted"] = set()
    game["gifs"] = {}
    game["votes"] = {}

    scenario = random.choice(SCENARIOS)
    game["used_scenarios"].append(scenario)

    await message.answer(f"🚀 راند 1\n\n😂 {scenario}")

# =========================
# 🎞 GIF HANDLER
# =========================
@dp.message(F.animation)
async def gif_handler(message: Message):
    game = get_game(message.chat.id)

    if not game["started"]:
        return

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    if uid in game["submitted"]:
        return await message.reply("⛔ قبلاً ارسال کردی")

    game["submitted"].add(uid)
    game["gifs"][uid] = message.animation.file_id

    if len(game["submitted"]) == len(game["players"]):
        await message.answer("🗳 رأی‌گیری شروع شد!")

# =========================
# 🏆 SCOREBOARD
# =========================
@dp.message(Command("scoreboard"))
async def scoreboard(message: Message):
    game = get_game(message.chat.id)

    ranking = sorted(game["scores"].items(), key=lambda x: x[1], reverse=True)

    text = "🏆 SCOREBOARD\n\n"
    for i, (uid, score) in enumerate(ranking, 1):
        text += f"{i}. {game['players'][uid]} - {score}\n"

    await message.answer(text)

# =========================
# 🏁 END GAME
# =========================
@dp.message(Command("end_game"))
async def end_game(message: Message):
    game = get_game(message.chat.id)

    ranking = sorted(game["scores"].items(), key=lambda x: x[1], reverse=True)

    text = "🏁 FINAL RESULT\n\n"

    for i, (uid, score) in enumerate(ranking, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
        text += f"{medal} {game['players'][uid]} - {score}\n"

    games[message.chat.id] = {
        "started": False,
        "players": {},
        "round": 0,
        "submitted": set(),
        "scores": {},
        "gifs": {},
        "used_scenarios": [],
        "votes": {}
    }

    await message.answer(text)

# =========================
# 🚀 RUN BOT
# =========================
async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
