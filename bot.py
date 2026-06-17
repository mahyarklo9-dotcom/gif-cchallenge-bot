from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command

import asyncio
import os
import random

# =========================
# BOT
# =========================

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN is not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# =========================
# CONFIG
# =========================

MAX_ROUNDS = 15

SUBMIT_TIME = 45
VOTE_TIME = 30

BOT_OFF = False

# =========================
# SCENARIOS
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

# =========================
# GAME STORAGE
# =========================

games = {}

# =========================
# GAME TEMPLATE
# =========================

def create_game():

    return {
        "started": False,
        "host": None,
        "players": {},
        "scores": {},
        "round": 0,
        "scenario": None,
        "used": [],
        "submit_open": False,
        "vote_open": False,
        "submitted": set(),
        "entries": {},
        "votes": {},
        "vote_count": {}
    }

# =========================
# GET GAME
# =========================

def get_game(chat_id):

    if chat_id not in games:
        games[chat_id] = create_game()

    return games[chat_id]

# =========================
# BOT STATE
# =========================

def bot_disabled():

    return BOT_OFF

# =========================
# SCENARIO PICKER
# =========================

def new_scenario(game):

    available = [
        s for s in SCENARIOS
        if s not in game["used"]
    ]

    if not available:

        game["used"] = []
        available = SCENARIOS.copy()

    scenario = random.choice(available)

    game["used"].append(scenario)

    return scenario

# =========================
# RESET ROUND
# =========================

def reset_round(game):

    game["submitted"] = set()
    game["entries"] = {}
    game["votes"] = {}
    game["vote_count"] = {}
    game["submit_open"] = False
    game["vote_open"] = False

# =========================
# BASIC COMMANDS
# =========================

@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "🤖 ربات مسابقه میم آماده است.\n\n"
        "/helpp"
    )

@dp.message(Command("helpp"))
async def helpp(message: Message):

    await message.answer(
        "📌 دستورات:\n\n"
        "/newgame\n"
        "/join\n"
        "/startgame\n"
        "/scoreboard\n"
        "/stopgame\n\n"
        "⚙️ مدیریت:\n"
        "/die\n"
        "/live"
    )

# =========================
# POWER COMMANDS
# =========================

@dp.message(Command("die"))
async def die(message: Message):

    global BOT_OFF

    BOT_OFF = True

    await message.answer(
        "🔴 ربات خاموش شد"
    )

@dp.message(Command("live"))
async def live(message: Message):

    global BOT_OFF

    BOT_OFF = False

    await message.answer(
        "🟢 ربات روشن شد"
    )
    # =========================
# NEW GAME
# =========================

@dp.message(Command("newgame"))
async def newgame(message: Message):

    if bot_disabled():
        return

    chat_id = message.chat.id

    games[chat_id] = create_game()

    game = games[chat_id]

    game["host"] = message.from_user.id

    game["players"] = {
        message.from_user.id:
        message.from_user.first_name
    }

    game["scores"] = {
        message.from_user.id: 0
    }

    await message.answer(
        "🎮 بازی جدید ساخته شد.\n\n"
        "بازیکنان با /join وارد شوند."
    )

# =========================
# JOIN
# =========================

@dp.message(Command("join"))
async def join(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if game["host"] is None:

        await message.answer(
            "❌ ابتدا /newgame اجرا شود."
        )
        return

    uid = message.from_user.id

    if uid in game["players"]:

        await message.answer(
            "⚠️ قبلاً وارد بازی شده‌ای."
        )
        return

    game["players"][uid] = (
        message.from_user.first_name
    )

    game["scores"][uid] = 0

    await message.answer(
        f"✅ {message.from_user.first_name} وارد بازی شد."
    )

# =========================
# SCOREBOARD
# =========================

@dp.message(Command("scoreboard"))
async def scoreboard(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if not game["players"]:

        await message.answer(
            "❌ هنوز بازی ساخته نشده."
        )
        return

    ranking = sorted(
        game["scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    text = "🏆 جدول امتیازات\n\n"

    place = 1

    for uid, score in ranking:

        text += (
            f"{place}. "
            f"{game['players'][uid]}"
            f" ➜ {score}\n"
        )

        place += 1

    await message.answer(text)

# =========================
# START GAME
# =========================

@dp.message(Command("startgame"))
async def startgame(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if game["host"] is None:

        await message.answer(
            "❌ ابتدا /newgame اجرا شود."
        )
        return

    if len(game["players"]) < 2:

        await message.answer(
            "❌ حداقل ۲ بازیکن لازم است."
        )
        return

    if game["started"]:

        await message.answer(
            "⚠️ بازی در حال اجراست."
        )
        return

    game["started"] = True

    game["round"] = 1

    await message.answer(
        "🚀 بازی شروع شد."
    )

    await start_round(
        message.chat.id
    )

# =========================
# START ROUND
# =========================

async def start_round(chat_id):

    game = get_game(chat_id)

    reset_round(game)

    game["submit_open"] = True

    scenario = new_scenario(game)

    game["scenario"] = scenario

    await bot.send_message(
        chat_id,
        f"🎯 راند {game['round']} از {MAX_ROUNDS}\n\n"
        f"😂 سناریو:\n"
        f"{scenario}\n\n"
        f"📸 عکس، استیکر یا GIF ارسال کنید.\n"
        f"⏳ زمان: {SUBMIT_TIME} ثانیه"
    )

    asyncio.create_task(
        submit_timer(chat_id)
    )

# =========================
# SUBMIT TIMER
# =========================

async def submit_timer(chat_id):

    await asyncio.sleep(
        SUBMIT_TIME
    )

    game = get_game(chat_id)

    if not game["started"]:
        return

    if not game["submit_open"]:
        return

    game["submit_open"] = False

    await bot.send_message(
        chat_id,
        "⌛ زمان ارسال آثار تمام شد."
    )

    if len(game["entries"]) == 0:

        await bot.send_message(
            chat_id,
            "❌ هیچ اثری ارسال نشد."
        )

        await finish_game(chat_id)

        return

    await start_vote(chat_id)
    # =========================
# PHOTO SUBMISSION
# =========================

@dp.message(F.photo)
async def receive_photo(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if not game["started"]:
        return

    if not game["submit_open"]:
        return

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    if uid in game["submitted"]:

        await message.reply(
            "⚠️ در این راند قبلاً اثر فرستاده‌ای."
        )
        return

    file_id = message.photo[-1].file_id

    game["submitted"].add(uid)

    game["entries"][uid] = {
        "type": "photo",
        "file_id": file_id
    }

    await message.reply(
        "✅ عکس ثبت شد."
    )

# =========================
# STICKER SUBMISSION
# =========================

@dp.message(F.sticker)
async def receive_sticker(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if not game["started"]:
        return

    if not game["submit_open"]:
        return

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    if uid in game["submitted"]:

        await message.reply(
            "⚠️ در این راند قبلاً اثر فرستاده‌ای."
        )
        return

    game["submitted"].add(uid)

    game["entries"][uid] = {
        "type": "sticker",
        "file_id": message.sticker.file_id
    }

    await message.reply(
        "✅ استیکر ثبت شد."
    )

# =========================
# GIF SUBMISSION
# =========================

@dp.message(F.animation)
async def receive_animation(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if not game["started"]:
        return

    if not game["submit_open"]:
        return

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    if uid in game["submitted"]:

        await message.reply(
            "⚠️ در این راند قبلاً اثر فرستاده‌ای."
        )
        return

    game["submitted"].add(uid)

    game["entries"][uid] = {
        "type": "animation",
        "file_id": message.animation.file_id
    }

    await message.reply(
        "✅ GIF ثبت شد."
    )

# =========================
# INVALID MEDIA
# =========================

@dp.message()
async def catch_other_messages(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if not game["started"]:
        return

    if not game["submit_open"]:
        return

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    await message.reply(
        "📌 فقط عکس، استیکر یا GIF مجاز است."
    )
    # =========================
# START VOTE
# =========================

async def start_vote(chat_id):

    game = get_game(chat_id)

    game["vote_open"] = True

    await bot.send_message(
        chat_id,
        "🗳 مرحله رأی‌گیری آغاز شد.\n"
        f"⏳ {VOTE_TIME} ثانیه فرصت دارید رأی بدهید."
    )

    index = 1

    for uid, media in game["entries"].items():

        game["vote_count"][uid] = 0

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"👍 رأی به اثر {index}",
                        callback_data=f"vote:{uid}"
                    )
                ]
            ]
        )

        caption = (
            f"🎭 اثر شماره {index}"
        )

        if media["type"] == "photo":

            await bot.send_photo(
                chat_id,
                media["file_id"],
                caption=caption,
                reply_markup=keyboard
            )

        elif media["type"] == "animation":

            await bot.send_animation(
                chat_id,
                media["file_id"],
                caption=caption,
                reply_markup=keyboard
            )

        elif media["type"] == "sticker":

            await bot.send_sticker(
                chat_id,
                media["file_id"]
            )

            await bot.send_message(
                chat_id,
                caption,
                reply_markup=keyboard
            )

        index += 1

    asyncio.create_task(
        vote_timer(chat_id)
    )

# =========================
# VOTE HANDLER
# =========================

@dp.callback_query(F.data.startswith("vote:"))
async def vote_handler(callback: CallbackQuery):

    game = get_game(
        callback.message.chat.id
    )

    if not game["vote_open"]:

        await callback.answer(
            "⛔ رأی‌گیری بسته شده است.",
            show_alert=True
        )
        return

    voter = callback.from_user.id

    if voter not in game["players"]:

        await callback.answer(
            "⛔ عضو بازی نیستی.",
            show_alert=True
        )
        return

    target = int(
        callback.data.split(":")[1]
    )

    if voter == target:

        await callback.answer(
            "❌ نمی‌توانی به خودت رأی بدهی.",
            show_alert=True
        )
        return

    if voter in game["votes"]:

        old_target = game["votes"][voter]

        game["vote_count"][old_target] -= 1

    game["votes"][voter] = target

    game["vote_count"][target] += 1

    await callback.answer(
        "✅ رأی ثبت شد."
    )

# =========================
# VOTE TIMER
# =========================

async def vote_timer(chat_id):

    await asyncio.sleep(VOTE_TIME)

    game = get_game(chat_id)

    if not game["started"]:
        return

    if not game["vote_open"]:
        return

    game["vote_open"] = False

    await bot.send_message(
        chat_id,
        "⌛ زمان رأی‌گیری تمام شد."
    )

    await calculate_round(chat_id)
    # =========================
# ROUND RESULT
# =========================

async def calculate_round(chat_id):

    game = get_game(chat_id)

    result_text = (
        f"📊 نتایج راند {game['round']}\n\n"
    )

    ranking = sorted(
        game["vote_count"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    for uid, votes in ranking:

        game["scores"][uid] += votes

        result_text += (
            f"👤 {game['players'][uid]}\n"
            f"🗳 رأی: {votes}\n"
            f"🏆 امتیاز کل: "
            f"{game['scores'][uid]}\n\n"
        )

    await bot.send_message(
        chat_id,
        result_text
    )

    await show_scoreboard(chat_id)

    if game["round"] >= MAX_ROUNDS:

        await finish_game(chat_id)
        return

    game["round"] += 1

    await bot.send_message(
        chat_id,
        f"⏭ آماده‌سازی راند {game['round']}..."
    )

    await asyncio.sleep(5)

    await start_round(chat_id)

# =========================
# SCOREBOARD
# =========================

async def show_scoreboard(chat_id):

    game = get_game(chat_id)

    ranking = sorted(
        game["scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    text = "🏆 جدول امتیازات\n\n"

    place = 1

    for uid, score in ranking:

        text += (
            f"{place}. "
            f"{game['players'][uid]}"
            f" ➜ {score}\n"
        )

        place += 1

    await bot.send_message(
        chat_id,
        text
    )
    # =========================
# FINISH GAME
# =========================

async def finish_game(chat_id):

    game = get_game(chat_id)

    ranking = sorted(
        game["scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    if not ranking:

        games[chat_id] = create_game()
        return

    winner_id = ranking[0][0]
    winner_score = ranking[0][1]

    text = (
        "🎉 بازی به پایان رسید!\n\n"
        f"🥇 برنده: "
        f"{game['players'][winner_id]}\n"
        f"🏆 امتیاز: {winner_score}\n\n"
        "📊 رتبه‌بندی نهایی:\n\n"
    )

    place = 1

    for uid, score in ranking:

        text += (
            f"{place}. "
            f"{game['players'][uid]}"
            f" ➜ {score}\n"
        )

        place += 1

    await bot.send_message(
        chat_id,
        text
    )

    games[chat_id] = create_game()

# =========================
# STOP GAME
# =========================

@dp.message(Command("stopgame"))
async def stopgame(message: Message):

    if bot_disabled():
        return

    game = get_game(message.chat.id)

    if not game["started"]:

        await message.answer(
            "❌ بازی فعالی وجود ندارد."
        )
        return

    await bot.send_message(
        message.chat.id,
        "🛑 بازی توسط مدیر متوقف شد."
    )

    await finish_game(
        message.chat.id
    )

# =========================
# MAIN
# =========================

async def main():

    print("BOT STARTED")

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
