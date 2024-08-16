import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Handlers
@dp.message(Command(commands=["start", "help"]))
async def command_start_handler(message: types.Message):
    """ 
    This handler receives messages with '/start' or '/help' command 
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by aiogram.")

@dp.message()
async def echo(message: types.Message):
    """
    This will return echo
    """
    await message.answer(message.text)

async def main():
    # Start polling
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
