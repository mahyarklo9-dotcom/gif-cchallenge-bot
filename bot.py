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
            "players": {},
            "round": 0,
            "submitted": set()
        }

    return games[chat_id]


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🎉 ربات GIF Challenge فعال است!\n\n"
        "برای دیدن راهنما:\n"
        "/helpp"
    )


@dp.message(Command("helpp"))
async def helpp(message: Message):
    await message.answer(
        "🎮 راهنمای بازی\n\n"
        "🆕 /newgame\n"
        "ساخت بازی جدید\n\n"
        "👤 /join\n"
        "ورود به بازی\n\n"
        "👥 /players\n"
        "نمایش بازیکنان\n\n"
        "🚀 /startgame\n"
        "شروع بازی\n\n"
        "🛑 /end_game\n"
        "پایان بازی\n\n"
        "🎯 نحوه بازی:\n"
        "ربات یک موقعیت خنده‌دار ارسال می‌کند.\n"
        "همه بازیکنان یک GIF می‌فرستند.\n"
        "بعد از ارسال همه GIFها، راند بعدی شروع می‌شود."
    )


@dp.message(Command("newgame"))
async def newgame(message: Message):
    game = get_game(message.chat.id)

    game["started"] = False
    game["players"] = {}
    game["round"] = 0
    game["submitted"] = set()

    await message.answer(
        "🎮 بازی جدید ساخته شد!\n\n"
        "⏳ منتظر بازیکنان...\n\n"
        "برای ورود:\n"
        "/join"
    )


@dp.message(Command("join"))
async def join(message: Message):
    game = get_game(message.chat.id)

    if game["started"]:
        await message.answer("⚠️ بازی شروع شده است.")
        return

    user_id = message.from_user.id

    if user_id in game["players"]:
        await message.answer("⚠️ شما قبلاً وارد بازی شده‌اید.")
        return

    game["players"][user_id] = message.from_user.first_name

    await message.answer(
        f"✅ {message.from_user.first_name} وارد بازی شد.\n\n"
        f"👥 تعداد بازیکنان: {len(game['players'])}"
    )


@dp.message(Command("players"))
async def players(message: Message):
    game = get_game(message.chat.id)

    if not game["players"]:
        await message.answer("❌ هنوز بازیکنی وارد نشده است.")
        return

    text = "👥 بازیکنان حاضر:\n\n"

    for i, player in enumerate(game["players"].values(), start=1):
        text += f"{i}. {player}\n"

    text += "\n🚀 /startgame"

    await message.answer(text)


@dp.message(Command("startgame"))
async def startgame(message: Message):
    game = get_game(message.chat.id)

    if len(game["players"]) < 2:
        await message.answer("❌ حداقل ۲ بازیکن لازم است.")
        return

    if game["started"]:
        await message.answer("⚠️ بازی قبلاً شروع شده است.")
        return

    game["started"] = True
    game["round"] = 1
    game["submitted"] = set()

    scenario = random.choice(SCENARIOS)

    await message.answer(
        f"🚀 بازی شروع شد!\n\n"
        f"🎯 راند {game['round']}\n\n"
        f"😂 {scenario}\n\n"
        "📤 همه بازیکنان یک GIF ارسال کنند."
    )


@dp.message(Command("end_game"))
async def end_game(message: Message):
    game = get_game(message.chat.id)

    if not game["started"]:
        await message.answer("⚠️ بازی فعالی وجود ندارد.")
        return

    game["started"] = False
    game["players"] = {}
    game["round"] = 0
    game["submitted"] = set()

    await message.answer(
        "🏁 بازی پایان یافت.\n\n"
        "برای شروع مجدد:\n"
        "/newgame"
    )


@dp.message(F.animation)
async def gif_handler(message: Message):
    game = get_game(message.chat.id)

    if not game["started"]:
        return

    user_id = message.from_user.id

    if user_id not in game["players"]:
        return

    if user_id in game["submitted"]:
        await message.reply(
            "⛔ شما قبلاً GIF این راند را ارسال کرده‌اید."
        )
        return

    game["submitted"].add(user_id)

    remaining = len(game["players"]) - len(game["submitted"])

    await message.reply(
        f"✅ GIF ثبت شد.\n"
        f"⏳ {remaining} بازیکن باقی مانده است."
    )

    if len(game["submitted"]) == len(game["players"]):
        await message.answer("🎉 همه GIF ها دریافت شد!")

        await asyncio.sleep(2)

        game["round"] += 1
        game["submitted"] = set()

        scenario = random.choice(SCENARIOS)

        await message.answer(
            f"🎯 راند {game['round']}\n\n"
            f"😂 {scenario}\n\n"
            "📤 GIF بعدی خود را ارسال کنید."
        )


async def main():
    print("Bot Started...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
