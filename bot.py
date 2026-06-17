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

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN is not set")

bot = Bot(token=TOKEN)
dp = Dispatcher()

MAX_ROUNDS = 15

games = {}

SCENARIOS =[
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

            "gifs": {},

            "votes": {},

            "used_scenarios": [],

            "voting": False,

            "current_scenario": None
        }

    return games[chat_id]


def get_new_scenario(game):

    available = [

        s

        for s in SCENARIOS

        if s not in game["used_scenarios"]
    ]

    if not available:

        game["used_scenarios"] = []

        available = SCENARIOS.copy()

    scenario = random.choice(
        available
    )

    game["used_scenarios"].append(
        scenario
    )

    return scenario


# =========================
# HELP
# =========================

@dp.message(Command("help"))
async def help_alias(message: Message):

    await helpp(message)


@dp.message(Command("helpp"))
async def helpp(message: Message):

    text = """
🎮 راهنمای کامل GIF Challenge

/start
فعال سازی ربات

/help
نمایش راهنما

/info
اطلاعات سازنده

/newgame
ساخت بازی جدید

/join
ورود به بازی

/players
نمایش بازیکنان

/startgame
شروع بازی

/scoreboard
نمایش جدول امتیازات

/endvote
پایان رأی گیری توسط Host

/end_game
پایان بازی توسط Host

📌 قوانین

• فقط در گروه کار می‌کند
• حداقل ۲ بازیکن لازم است
• هر بازی ۱۵ راند دارد
• هر نفر فقط یک GIF در هر راند
• هر نفر می‌تواند به چند GIF رأی بدهد
• رأی به خود ممنوع است
• در صورت مساوی همه برندگان امتیاز می‌گیرند
• بعد از راند ۱۵ بازی تمام می‌شود
"""

    await message.answer(text)
    # =========================
# INFO
# =========================

@dp.message(Command("info"))
async def info(message: Message):

    await message.answer(
        "🎮 GIF Challenge Bot\n\n"
        "🛠 سازنده: @Jack_landon\n"
        "⚡ نسخه: 2.0\n"
        "🎯 بازی گروهی GIF Challenge\n"
        "📖 راهنما: /help"
    )


# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "🎮 GIF Challenge Bot فعال شد!\n\n"
        "برای ساخت بازی:\n"
        "/newgame\n\n"
        "برای راهنما:\n"
        "/help"
    )


# =========================
# NEW GAME
# =========================

@dp.message(Command("newgame"))
async def newgame(message: Message):

    if message.chat.type not in [
        "group",
        "supergroup"
    ]:
        return await message.answer(
            "❌ این بازی فقط داخل گروه کار می‌کند"
        )

    current = get_game(
        message.chat.id
    )

    if current["started"]:

        return await message.answer(
            "⚠️ یک بازی در حال اجراست"
        )

    host_id = message.from_user.id

    games[message.chat.id] = {

        "started": False,

        "host": host_id,

        "players": {
            host_id:
            message.from_user.first_name
        },

        "scores": {
            host_id: 0
        },

        "round": 0,

        "submitted": set(),

        "gifs": {},

        "votes": {},

        "used_scenarios": [],

        "voting": False,

        "current_scenario": None
    }

    await message.answer(
        f"🎮 بازی جدید ساخته شد\n\n"
        f"👑 Host: {message.from_user.first_name}\n"
        f"✅ Host به بازی اضافه شد\n\n"
        f"برای ورود:\n"
        f"/join"
    )


# =========================
# JOIN
# =========================

@dp.message(Command("join"))
async def join(message: Message):

    game = get_game(
        message.chat.id
    )

    if game["host"] is None:

        return await message.answer(
            "❌ ابتدا /newgame اجرا شود"
        )

    if game["started"]:

        return await message.answer(
            "⚠️ بازی شروع شده است"
        )

    uid = message.from_user.id

    if uid in game["players"]:

        return await message.answer(
            "⚠️ قبلاً وارد بازی شدی"
        )

    game["players"][uid] = (
        message.from_user.first_name
    )

    game["scores"][uid] = 0

    await message.answer(
        f"✅ {message.from_user.first_name} وارد بازی شد"
    )


# =========================
# PLAYERS
# =========================

@dp.message(Command("players"))
async def players(message: Message):

    game = get_game(
        message.chat.id
    )

    if not game["players"]:

        return await message.answer(
            "❌ هنوز بازیکنی وجود ندارد"
        )

    text = "👥 بازیکنان بازی\n\n"

    for i, name in enumerate(
        game["players"].values(),
        start=1
    ):

        text += f"{i}. {name}\n"

    await message.answer(text)
    # =========================
# START GAME
# =========================

@dp.message(Command("startgame"))
async def startgame(message: Message):

    game = get_game(
        message.chat.id
    )

    if game["host"] != message.from_user.id:

        return await message.answer(
            "⛔ فقط Host می‌تواند بازی را شروع کند"
        )

    if game["started"]:

        return await message.answer(
            "⚠️ بازی قبلاً شروع شده است"
        )

    if len(game["players"]) < 2:

        return await message.answer(
            "❌ حداقل ۲ بازیکن لازم است"
        )

    game["started"] = True

    game["round"] = 1

    game["submitted"] = set()

    game["gifs"] = {}

    game["votes"] = {}

    game["voting"] = False

    scenario = get_new_scenario(
        game
    )

    game["current_scenario"] = scenario

    await message.answer(
        f"🚀 راند 1 از {MAX_ROUNDS}\n\n"
        f"😂 {scenario}\n\n"
        f"🎞 هر بازیکن یک GIF ارسال کند"
    )


# =========================
# SCOREBOARD
# =========================

@dp.message(Command("scoreboard"))
async def scoreboard(message: Message):

    game = get_game(
        message.chat.id
    )

    if not game["scores"]:

        return await message.answer(
            "❌ امتیازی ثبت نشده"
        )

    ranking = sorted(
        game["scores"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    text = "🏆 SCOREBOARD\n\n"

    for i, (uid, score) in enumerate(
        ranking,
        start=1
    ):

        text += (
            f"{i}. "
            f"{game['players'][uid]}"
            f" - {score}\n"
        )

    await message.answer(text)


# =========================
# END VOTE
# =========================

@dp.message(Command("endvote"))
async def endvote(message: Message):

    game = get_game(
        message.chat.id
    )

    if game["host"] != message.from_user.id:

        return await message.answer(
            "⛔ فقط Host"
        )

    if not game["voting"]:

        return await message.answer(
            "❌ رأی گیری فعال نیست"
        )

    await finish_round(
        message.chat.id
    )


# =========================
# END GAME
# =========================

@dp.message(Command("end_game"))
async def end_game(message: Message):

    game = get_game(
        message.chat.id
    )

    if game["host"] != message.from_user.id:

        return await message.answer(
            "⛔ فقط Host"
        )

    await end_game_internal(
        message.chat.id
    )
    # =========================
# GIF HANDLER
# =========================

@dp.message(F.animation)
async def gif_handler(message: Message):

    game = get_game(
        message.chat.id
    )

    if not game["started"]:
        return

    if game["voting"]:

        return await message.reply(
            "⛔ رأی گیری در حال انجام است"
        )

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    if uid in game["submitted"]:

        return await message.reply(
            "⛔ قبلاً GIF ارسال کردی"
        )

    game["submitted"].add(uid)

    game["gifs"][uid] = (
        message.animation.file_id
    )

    await message.reply(
        "✅ GIF ثبت شد"
    )

    if len(game["submitted"]) == len(game["players"]):

        game["voting"] = True

        asyncio.create_task(
            auto_finish_vote(
                message.chat.id
            )
        )

        await message.answer(
            "🗳 رأی گیری آغاز شد!"
        )

        for owner_id, gif_id in game["gifs"].items():

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=f"👍 رأی به {game['players'][owner_id]}",
                            callback_data=f"vote_{owner_id}"
                        )
                    ]
                ]
            )

            await bot.send_animation(
                chat_id=message.chat.id,
                animation=gif_id,
                reply_markup=keyboard
            )


# =========================
# GIF DOCUMENT
# =========================

@dp.message(F.document)
async def gif_document(
    message: Message
):

    if not message.document:
        return

    if (
        message.document.mime_type
        != "image/gif"
    ):
        return

    game = get_game(
        message.chat.id
    )

    if not game["started"]:
        return

    if game["voting"]:

        return await message.reply(
            "⛔ رأی گیری در حال انجام است"
        )

    uid = message.from_user.id

    if uid not in game["players"]:
        return

    if uid in game["submitted"]:

        return await message.reply(
            "⛔ قبلاً GIF ارسال کردی"
        )

    game["submitted"].add(uid)

    game["gifs"][uid] = (
        message.document.file_id
    )

    await message.reply(
        "✅ GIF ثبت شد"
    )


# =========================
# VOTE HANDLER
# =========================

@dp.callback_query(
    F.data.startswith("vote_")
)
async def vote_handler(
    call: CallbackQuery
):

    if not call.message:
        return

    game = get_game(
        call.message.chat.id
    )

    if not game["voting"]:

        return await call.answer(
            "⛔ رأی گیری بسته شده"
        )

    voter = call.from_user.id

    if voter not in game["players"]:

        return await call.answer(
            "عضو بازی نیستی"
        )

    try:

        target = int(
            call.data.split("_")[1]
        )

    except:

        return await call.answer(
            "خطا"
        )

    if voter == target:

        return await call.answer(
            "❌ نمی‌توانی به خودت رأی بدهی",
            show_alert=True
        )

    if voter not in game["votes"]:

        game["votes"][voter] = set()

    if target in game["votes"][voter]:

        return await call.answer(
            "⚠️ قبلاً رأی دادی"
        )

    game["votes"][voter].add(
        target
    )

    await call.answer(
        "✅ رأی ثبت شد"
    )


# =========================
# AUTO FINISH VOTE
# =========================

async def auto_finish_vote(
    chat_id
):

    await asyncio.sleep(
        120
    )

    game = get_game(
        chat_id
    )

    if game["voting"]:

        await finish_round(
            chat_id
        )


# =========================
# FINISH ROUND
# =========================

async def finish_round(chat_id):

    game = get_game(chat_id)

    if not game["started"]:
        return

    game["voting"] = False

    vote_count = {}

    for voter, targets in game["votes"].items():

        for target in targets:

            vote_count[target] = (
                vote_count.get(target, 0) + 1
            )

    if vote_count:

        max_vote = max(
            vote_count.values()
        )

        winners = [

            uid

            for uid, votes
            in vote_count.items()

            if votes == max_vote
        ]

        result_text = (
            f"🏆 نتیجه راند {game['round']}\n\n"
        )

        for uid in winners:

            game["scores"][uid] += 1

            result_text += (
                f"🥇 {game['players'][uid]}"
                f" (+1 امتیاز)\n"
            )

        await bot.send_message(
            chat_id,
            result_text
        )

    else:

        await bot.send_message(
            chat_id,
            "❌ هیچ رأیی ثبت نشد"
        )

    game["submitted"] = set()

    game["gifs"] = {}

    game["votes"] = {}

    if game["round"] >= MAX_ROUNDS:

        await end_game_internal(
            chat_id
        )

        return

    game["round"] += 1

    scenario = get_new_scenario(
        game
    )

    game["current_scenario"] = scenario

    await bot.send_message(

        chat_id,

        f"🚀 راند {game['round']} از {MAX_ROUNDS}\n\n"

        f"😂 {scenario}\n\n"

        f"🎞 هر بازیکن یک GIF ارسال کند"
    )


# =========================
# END GAME INTERNAL
# =========================

async def end_game_internal(
    chat_id
):

    game = get_game(
        chat_id
    )

    ranking = sorted(

        game["scores"].items(),

        key=lambda x: x[1],

        reverse=True
    )

    text = "🏁 پایان بازی\n\n"

    if ranking:

        best_score = ranking[0][1]

        champions = [

            uid

            for uid, score
            in ranking

            if score == best_score
        ]

        text += "👑 قهرمانان:\n\n"

        for uid in champions:

            text += (
                f"🏆 "
                f"{game['players'][uid]}"
                f" - "
                f"{best_score} امتیاز\n"
            )

        text += "\n"

    for i, (uid, score) in enumerate(
        ranking,
        start=1
    ):

        text += (
            f"{i}. "
            f"{game['players'][uid]}"
            f" - {score}\n"
        )

    await bot.send_message(
        chat_id,
        text
    )

    games.pop(
        chat_id,
        None
    )


# =========================
# UNKNOWN
# =========================

@dp.message()
async def unknown(
    message: Message
):

    await message.answer(
        "❓ دستور نامعتبر\n\n"
        "📖 راهنما:\n"
        "/help"
    )


# =========================
# MAIN
# =========================

async def main():

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )