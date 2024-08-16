import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from dotenv import load_dotenv
import os
import openai

class Reference:
    """
    A class to store the previous response from the ChatGPT API
    """
    def __init__(self) -> None:
        self.response = ""

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

def clear_past():
    """A function to clear the previous conversation and context."""
    reference.response = ""

@dp.message(Command(commands=["start"]))
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    await message.reply("Hi\nI am Perry the bot! Created by Perry. How can I assist you?")

@dp.message(Command(commands=["clear"]))
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")

@dp.message(Command(commands=["help"]))
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm a ChatGPT Telegram bot created by Perry! Please follow these commands:
    /start - to start the conversation
    /clear - to clear the past conversation and context
    /help - to get this help menu
    I hope this helps. :)
    """
    await message.reply(help_command)

@dp.message()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the ChatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    
    messages = []
    
    if reference.response:
        messages.append({"role": "assistant", "content": reference.response})
        
    messages.append({"role": "user", "content": message.text})

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages
    )
    
    reference.response = response.choices[0].message['content']
    print(f">>> ChatGPT: \n\t{reference.response}")
    await message.answer(reference.response)

async def main():
    await dp.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())
