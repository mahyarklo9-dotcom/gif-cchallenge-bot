from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

TOKEN = "8623719700:AAF0h0Q2g9sIozdR5XnVyneWi0_JUuZ-KGk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("ربات روشن است 🎉")

async def main():
    print("Bot Started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())