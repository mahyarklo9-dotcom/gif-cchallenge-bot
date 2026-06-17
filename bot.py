from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram import BaseMiddleware

import asyncio
import os
import random

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN is not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

MAX_ROUNDS = 15
SUBMIT_TIME = 45
VOTE_TIME = 30

BOT_DISABLED = False

# =========================
# MIDDLEWARE (FIXED)
# =========================

class DisableMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):

        global BOT_DISABLED

        if BOT_DISABLED:

            # فقط /live اجازه دارد
            if isinstance(event, Message):
                if event.text != "/live":
                    return
            else:
                return

        return await handler(event, data)


dp.message.middleware(DisableMiddleware())
dp.callback_query.middleware(DisableMiddleware())


# =========================
# GAME STATE
# =========================

games = {}

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
    "وقتی می‌فهمی کلاهت را ۳ ساعت روی سرت گذاشته بودی ولی برعکس!",
    "وقتی با اعتماد می‌گویی «این که کاری نداره» و بعد گیر می‌کنی!",
    "وقتی در جمع می‌خندی و بعد می‌پرسی «ببخشید به چی می‌خندید؟»!",
    "وقتی نان تست از دستت می‌افتد و دقیقاً سمت کره‌ای می‌خورد!",
    "وقتی می‌خواهی بی‌صدا وارد خانه شوی و در جیرجیر می‌کند!",
    "وقتی اسمت را صدا می‌زنند و تو از جایت می‌پری ولی منظورشان یکی دیگر بوده!",
    "وقتی خودت را جمع‌وجور می‌کنی که فوتبالیست‌طور توپ بزنی و می‌خوری زمین!",
    "وقتی برای عکس گرفتن آماده می‌شوی ولی دوربین بسته شده!",
    "وقتی گوشی را برداشتی تا ساعت را نگاه کنی و یادت می‌رود!",
    "وقتی می‌گویی «الان دقیق می‌دونم کجاست» و پنج دقیقه بعد هیچ‌چیز پیدا نمی‌کنی!",
    "وقتی به موهایت ژل زدی ولی باد از همه قوی‌تر است!",
    "وقتی توی صف می‌ایستی و می‌فهمی اصلاً صف مال تو نبوده!",
    "وقتی می‌خواهی از یک گفت‌وگوی خجالت‌آور فرار کنی و کسی صدایت می‌کند!",
    "وقتی وسط صحبت ناگهان یادت می‌رود داشتی چه می‌گفتی!",
    "وقتی چشم‌هایت را می‌بندی که نخوابی، ولی دقیقاً خوابت می‌برد!",
    "وقتی می‌خواهی چیزی را سریع بخوری و زبانت می‌سوزد!",
    "وقتی لباس جدید می‌پوشی و همان روز باران می‌آید!",
    "وقتی می‌خواهی خیلی جدی باشی ولی یک خنده ناگهانی همه‌چیز را خراب می‌کند!",
    "وقتی موقع سلام دادن، هم‌زمان می‌روی برای دست دادن و بغل!",
    "وقتی با شور و شوق وارد آشپزخانه می‌شوی و یادت می‌آید برای غذا نیامده بودی!",
    "وقتی لپ‌تاپت را باز می‌کنی و می‌بینی ۷۲ درصد شارژ دارد، ولی شارژرش آنجاست!",
    "وقتی دکمه ارسال را زدی و تازه فهمیدی غلط املایی داری!",
    "وقتی می‌خواهی بی‌صدا بخندی ولی صدات مثل غاز درمی‌آید!",
    "وقتی سعی می‌کنی از روی یک چیز کوچک بپری و خیلی نمایشی زمین می‌خوری!",
    "وقتی می‌خواهی منطقی صحبت کنی ولی عصبانیت اجازه نمی‌دهد!",
    "وقتی فکر می‌کنی یکی داره نگات می‌کنه، برمی‌گردی و واقعاً داره نگات می‌کنه!",
    "وقتی زنگ می‌زنی به دوستت و می‌گه الان داشتم بهت زنگ می‌زدم!",
    "وقتی کفشت را پیدا نمی‌کنی و می‌بینی یکی پای خودته!",
    "وقتی می‌خواهی آرام آب بخوری و ناگهان سرفه‌ات می‌گیرد!",
    "وقتی در مهمانی اسم کسی را فراموش می‌کنی و فقط لبخند می‌زنی!",
    "وقتی می‌خواهی خیلی حرفه‌ای فایل را ذخیره کنی و کامپیوتر هنگ می‌کند!",
    "وقتی با خودت می‌گویی فقط ۵ دقیقه می‌خوابم و ۳ ساعت بعد بیدار می‌شوی!",
    "وقتی چیزی را زمین می‌اندازی و همه دقیقاً نگاه می‌کنند!",
    "وقتی می‌خواهی از در رد شوی و لباست به دستگیره گیر می‌کند!",
    "وقتی می‌بینی چیزی که دنبالش بودی، دقیقاً جلوی چشمت بوده!",
    "وقتی می‌خواهی جدی باشی ولی یک اتفاق بی‌ربط کل فضا را منفجر می‌کند!"
]
def get_game(chat_id):

    if chat_id not in games:
        games[chat_id] = {
            "started": False,
            "host": None,
            "players": {},
            "scores": {},
            "round": 0,
            "submitted": set(),
            "media": {},
            "votes": {},
            "used": [],
            "voting": False,
            "submit_open": False,
            "scenario": None
        }

    return games[chat_id]


def new_scenario(game):

    available = [s for s in SCENARIOS if s not in game["used"]]

    if not available:
        game["used"] = []
        available = SCENARIOS.copy()

    s = random.choice(available)
    game["used"].append(s)
    return s


# =========================
# HELP
# =========================

@dp.message(Command("helpp"))
async def helpp(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎮 بازی", callback_data="help_game"),
                InlineKeyboardButton(text="⚙️ مدیریت", callback_data="help_admin")
            ],
            [
                InlineKeyboardButton(text="📌 قوانین", callback_data="help_rules")
            ]
        ]
    )

    await message.answer(
        "🎮 GIF Challenge\nیکی را انتخاب کن:",
        reply_markup=keyboard
    )


@dp.callback_query(F.data == "help_game")
async def help_game(call: CallbackQuery):

    await call.message.answer(
        "/newgame\n/join\n/startgame\n/players\n/scoreboard"
    )
    await call.answer()


@dp.callback_query(F.data == "help_admin")
async def help_admin(call: CallbackQuery):

    await call.message.answer(
        "/endvote\n/end_game\n/die\n/live"
    )
    await call.answer()


@dp.callback_query(F.data == "help_rules")
async def help_rules(call: CallbackQuery):

    await call.message.answer(
        "15 rounds\n45s send\n30s vote\nGIF/photo/sticker"
    )
    await call.answer()


# =========================
# DIE / LIVE
# =========================

@dp.message(Command("die"))
async def die(message: Message):
    global BOT_DISABLED
    BOT_DISABLED = True
    await message.answer("💀 OFF")


@dp.message(Command("live"))
async def live(message: Message):
    global BOT_DISABLED
    BOT_DISABLED = False
    await message.answer("🟢 ON")


# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Bot Ready\n/helpp")


# =========================
# NEW GAME
# =========================

@dp.message(Command("newgame"))
async def newgame(message: Message):

    game = get_game(message.chat.id)

    host = message.from_user.id

    game["host"] = host
    game["players"] = {host: message.from_user.first_name}
    game["scores"] = {host: 0}

    await message.answer("Game created")


# =========================
# JOIN
# =========================

@dp.message(Command("join"))
async def join(message: Message):

    game = get_game(message.chat.id)

    uid = message.from_user.id

    if uid in game["players"]:
        return

    game["players"][uid] = message.from_user.first_name
    game["scores"][uid] = 0

    await message.answer("Joined")


# =========================
# START GAME
# =========================

@dp.message(Command("startgame"))
async def startgame(message: Message):

    game = get_game(message.chat.id)

    if len(game["players"]) < 2:
        return await message.answer("Need 2 players")

    game["started"] = True
    game["round"] = 1
    game["submit_open"] = True

    game["scenario"] = new_scenario(game)

    await message.answer(
        f"Round 1\n\n{game['scenario']}"
    )


# =========================
# PLAYERS
# =========================

@dp.message(Command("players"))
async def players(message: Message):

    game = get_game(message.chat.id)

    text = "Players:\n"

    for p in game["players"].values():
        text += f"- {p}\n"

    await message.answer(text)


# =========================
# SCOREBOARD
# =========================

@dp.message(Command("scoreboard"))
async def scoreboard(message: Message):

    game = get_game(message.chat.id)

    text = "Score:\n"

    for uid, score in game["scores"].items():
        text += f"{game['players'][uid]}: {score}\n"

    await message.answer(text)


# =========================
# RUN
# =========================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
