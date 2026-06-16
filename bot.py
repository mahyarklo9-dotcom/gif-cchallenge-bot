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

SCENARIOS = [

# سناریوهای اصلی

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
"وقتی می‌گویی من دارم میرم و تازه لباس نپوشیدی!",
"وقتی با صدای بلند آهنگ می‌خوانی و می‌فهمی هدفونت وصل نبوده!",
"وقتی روی صندلی می‌نشینی و می‌فهمی از قبل خیس بوده!",
"وقتی می‌خواهی خیلی شیک حرف بزنی ولی زبانت می‌گیرد!",
"وقتی به سطل زباله می‌زنی ولی توپ نیست!",
"وقتی داری از پله‌ها پایین می‌آیی و یک پله کم می‌آوری!",
"وقتی پیام الان میام را فرستادی و هنوز از تخت بلند نشدی!",
"وقتی برای کسی دست تکان می‌دهی و می‌فهمی با تو نبوده!",
"وقتی در آسانسور فقط تویی و یک نفر دیگر!",
"وقتی می‌خواهی خونسرد باشی ولی لیوان از دستت می‌افتد!",
"وقتی فکر می‌کنی میکروفون خاموش است ولی روشن بوده!",
"وقتی وسط صحبت یادت می‌رود داشتی چی می‌گفتی!",
"وقتی گوشی دستته ولی دنبالش می‌گردی!",
"وقتی فکر می‌کنی کسی نگات می‌کنه و واقعاً داره نگات می‌کنه!",
"وقتی می‌خوای خفن باشی ولی زمین می‌خوری!",
"وقتی پیام رو اشتباهی برای گروه می‌فرستی!",
"وقتی وسط خنده سرفه می‌کنی!",
"وقتی می‌خوای سریع جواب بدی ولی اینترنت هنگ می‌کنه!",
"وقتی فکر می‌کنی زنگ خورد ولی تو ذهنت بوده!",
"وقتی در بسته‌ست ولی هلش می‌دی!",
"وقتی می‌خوای آروم در رو ببندی ولی کل خونه می‌لرزه!",
"وقتی فکر می‌کنی فیلمو دیدی ولی آخرش یادت نیست!",
"وقتی می‌خوای حرفه‌ای تایپ کنی ولی کیبورد قاطی می‌کنه!",
"وقتی می‌خوای از در رد شی ولی شیشه‌ایه!",
"وقتی فکر می‌کنی وای فای قطعه ولی رمز اشتباهه!",
"وقتی یه جوک می‌گی و خودت بیشتر می‌خندی!",
"وقتی می‌فهمی کل روز لباس را پشت و رو پوشیده بودی!",
"وقتی بعد از سلام کردن می‌فهمی طرف را نمی‌شناسی!",
"وقتی می‌گی من رژیمم و پنج دقیقه بعد پیتزا می‌خوری!",
"وقتی فکر می‌کنی تنها خونه‌ای ولی یکی از اتاق بیرون میاد!",
"وقتی معلم میگه داوطلب داریم؟ و چشمت تو چشمش میفته!",
"وقتی می‌خوای یواشکی بخندی ولی صدات می‌پیچه!",
"وقتی وارد استخر می‌شی و آب خیلی سردتر از چیزیه که فکر می‌کردی!",
"وقتی به کسی پیام میدی و بعد می‌بینی یک سال پیش آنلاین بوده!",
"وقتی می‌خوای شجاع باشی ولی یه سوسک ظاهر میشه!",
"وقتی می‌فهمی جلسه‌ای که براش آماده شدی فرداست!",
"وقتی جلوی همه زمین می‌خوری ولی وانمود می‌کنی چیزی نشده!",
"وقتی فکر می‌کنی دوربین خاموشه!",
"وقتی تازه فهمیدی امروز دوشنبه است!",
"وقتی می‌خوای آروم بخوری ولی غذا روی لباست می‌ریزه!",
"وقتی رمز را درست وارد می‌کنی ولی CAPS LOCK روشنه!",
"وقتی وسط دعوا اسمت را اشتباه صدا می‌زنند!",
"وقتی به آینه لبخند می‌زنی و خودت می‌ترسی!",
"وقتی می‌فهمی پیام صوتی ۵ دقیقه‌ای اشتباه ارسال شده!",
"وقتی می‌خوای زرنگ باشی ولی لو میری!",
"وقتی می‌فهمی کل مدت هندزفری وصل نبوده!",
"وقتی وارد کلاس اشتباه می‌شی!",
"وقتی بیدار می‌شی و نمی‌دونی صبحه یا شبه!",
"وقتی از کسی تعریف می‌کنی و پشت سرت ایستاده!",
"وقتی می‌گی فقط یک قسمت سریال!",
"وقتی به در می‌کوبی و خودت می‌ترسی!",
"وقتی دنبال عینکت می‌گردی و روی چشمت بوده!",
"وقتی یخچال را باز می‌کنی و یادت میره چی می‌خواستی!",
"وقتی با اطمینان جواب میدی و اشتباهه!",
"وقتی می‌خوای عکس جدی بگیری ولی خنده‌ات می‌گیره!",
"وقتی می‌خوای فرار کنی ولی راه خروج اشتباهه!",
"وقتی می‌گی فقط پنج دقیقه می‌خوابم!",
"وقتی صدای خودتو توی ویس می‌شنوی!",
"وقتی برای اولین بار غذای خودت رو می‌پزی!",
"وقتی می‌خوای کمک کنی ولی اوضاع بدتر میشه!",
"وقتی از چیزی می‌ترسی که وجود نداره!",
"وقتی می‌خوای مخفی بشی ولی همه می‌بیننت!",
"وقتی از پشت شیشه به کسی سلام می‌کنی!",
"وقتی می‌فهمی شارژرت را جا گذاشتی!",
"وقتی وارد مغازه می‌شی و چیزی نمی‌خری!",
"وقتی می‌گی من کنترل اوضاع را دارم!"
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

            "voted_users": set(),

            "used_scenarios": [],

            "voting": False
        }

    return games[chat_id]


def get_new_scenario(game):

    available = [
        s for s in SCENARIOS
        if s not in game["used_scenarios"]
    ]

    if not available:
        game["used_scenarios"] = []
        available = SCENARIOS.copy()

    scenario = random.choice(available)

    game["used_scenarios"].append(scenario)

    return scenario
    # =========================
# HELP
# =========================

@dp.message(Command("helpp"))
async def helpp(message: Message):

    text = """
🎮 راهنمای GIF Challenge

/start
فعال سازی ربات

/info
اطلاعات سازنده

/newgame
ساخت بازی جدید

/join
ورود به بازی

/startgame
شروع بازی

/scoreboard
جدول امتیازات

/end_game
پایان بازی

📌 قوانین

• بازی فقط در گروه انجام می‌شود
• هر بازی ۱۵ راند دارد
• هر نفر فقط یک GIF در هر راند
• هر نفر می‌تواند به چند GIF رأی دهد
• رأی به خود مجاز نیست
• در مساوی همه برندگان امتیاز می‌گیرند
• پس از راند ۱۵ بازی خودکار تمام می‌شود
"""

    await message.answer(text)


# =========================
# INFO
# =========================

@dp.message(Command("info"))
async def info(message: Message):

    await message.answer(
        "🛠 ساخته شده توسط @Jack_landon"
    )


# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: Message):

    await message.answer(
        "🎮 GIF Challenge Bot فعال شد\n\n/newgame"
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
            "❌ فقط داخل گروه"
        )

    games[message.chat.id] = {

        "started": False,

        "host": message.from_user.id,

        "players": {},

        "scores": {},

        "round": 0,

        "submitted": set(),

        "gifs": {},

        "votes": {},

        "voted_users": set(),

        "used_scenarios": [],

        "voting": False
    }

    await message.answer(
        f"🎮 بازی جدید ساخته شد\n\n"
        f"👑 Host: {message.from_user.first_name}\n\n"
        f"/join"
    )


# =========================
# JOIN
# =========================

@dp.message(Command("join"))
async def join(message: Message):

    game = get_game(message.chat.id)

    if game["started"]:

        return await message.answer(
            "⚠️ بازی شروع شده"
        )

    uid = message.from_user.id

    if uid in game["players"]:

        return await message.answer(
            "⚠️ قبلاً وارد شدی"
        )

    game["players"][uid] = (
        message.from_user.first_name
    )

    game["scores"][uid] = 0

    await message.answer(
        f"✅ {message.from_user.first_name} وارد بازی شد"
    )


# =========================
# START GAME
# =========================

@dp.message(Command("startgame"))
async def startgame(message: Message):

    game = get_game(message.chat.id)

    if game["host"] != message.from_user.id:

        return await message.answer(
            "⛔ فقط Host می‌تواند بازی را شروع کند"
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

    game["voted_users"] = set()

    scenario = get_new_scenario(game)

    await message.answer(

        f"🚀 راند 1 از {MAX_ROUNDS}\n\n"
        f"😂 {scenario}\n\n"
        f"🎞 GIF مناسب را ارسال کنید"
    )


# =========================
# SCOREBOARD
# =========================

@dp.message(Command("scoreboard"))
async def scoreboard(message: Message):

    game = get_game(message.chat.id)

    if not game["scores"]:

        return await message.answer(
            "امتیازی ثبت نشده"
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
# END GAME
# =========================

@dp.message(Command("end_game"))
async def end_game(message: Message):

    game = get_game(message.chat.id)

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

    game = get_game(message.chat.id)

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

        await message.answer(
            "📌 می‌توانید به چند GIF رأی بدهید\n"
            "❌ رأی به خود مجاز نیست"
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

    game = get_game(
        call.message.chat.id
    )

    if not game["voting"]:

        return await call.answer(
            "رأی گیری بسته شده"
        )

    voter = call.from_user.id

    if voter not in game["players"]:

        return await call.answer(
            "عضو بازی نیستی"
        )

    target = int(
        call.data.split("_")[1]
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
            "قبلاً رأی دادی"
        )

    game["votes"][voter].add(
        target
    )

    await call.answer(
        "✅ رأی ثبت شد"
    )

    total_votes = sum(
        len(v)
        for v in game["votes"].values()
    )

    players_count = len(
        game["players"]
    )

    max_votes_needed = (
        players_count *
        (players_count - 1)
    )

    if total_votes >= max_votes_needed:

        await finish_round(
            call.message.chat.id
        )
        # =========================
# FINISH ROUND
# =========================

async def finish_round(chat_id):

    game = get_game(chat_id)

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

        result_text += (
            f"\n📊 تعداد رأی برنده: "
            f"{max_vote}"
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

    game["voted_users"] = set()

    if game["round"] >= MAX_ROUNDS:

        await end_game_internal(
            chat_id
        )

        return

    game["round"] += 1

    scenario = get_new_scenario(
        game
    )

    await bot.send_message(

        chat_id,

        f"🚀 راند "
        f"{game['round']} از "
        f"{MAX_ROUNDS}\n\n"

        f"😂 {scenario}\n\n"

        f"🎞 GIF ارسال کنید"
    )


# =========================
# END GAME INTERNAL
# =========================

async def end_game_internal(
    chat_id
):

    game = get_game(chat_id)

    ranking = sorted(

        game["scores"].items(),

        key=lambda x: x[1],

        reverse=True
    )

    text = (
        "🏁 پایان بازی\n\n"
    )

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
                f"{best_score}\n"
            )

        text += "\n"

    for i, (uid, score) in enumerate(
        ranking,
        start=1
    ):

        if i == 1:
            medal = "🥇"

        elif i == 2:
            medal = "🥈"

        elif i == 3:
            medal = "🥉"

        else:
            medal = "🏅"

        text += (
            f"{medal} "
            f"{game['players'][uid]}"
            f" - {score}\n"
        )

    await bot.send_message(
        chat_id,
        text
    )

    games[chat_id] = {

        "started": False,

        "host": None,

        "players": {},

        "scores": {},

        "round": 0,

        "submitted": set(),

        "gifs": {},

        "votes": {},

        "voted_users": set(),

        "used_scenarios": [],

        "voting": False
    }


# =========================
# UNKNOWN COMMAND
# =========================

@dp.message()
async def unknown(
    message: Message
):

    await message.answer(
        "❓ دستور نامعتبر\n\n"
        "برای راهنما:\n"
        "/helpp"
    )


# =========================
# MAIN
# =========================

async def main():

    print(
        "GIF Challenge Bot Started..."
    )

    await dp.start_polling(
        bot
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
