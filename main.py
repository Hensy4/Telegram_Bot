import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

BOT_TOKEN = "8992122596:AAFZkWeWXeIqGRG6U_MwDspVjTQ1n7ES0Hc"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Я бот-помощник 👋")
    
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())