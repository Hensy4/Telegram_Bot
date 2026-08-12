import random
import string
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

BOT_TOKEN = "8992122596:AAFZkWeWXeIqGRG6U_MwDspVjTQ1n7ES0Hc"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ====================
# password start
class PasswordGenerator:
    def __init__(self):
        self._password = ""
        
    def generate(self, length):
        all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + "!@#$%^&*()_+-="
        self._password = ''.join(random.choice(all_chars) for _ in range(length))
        return self._password

password_gen = PasswordGenerator()

@dp.message(Command("password"))
async def handle_password(message: Message):
    password = password_gen.generate(8)
    await message.answer(f"Твой пароль: {password}")

# ====================
# password stop 


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Я бот-помощник 👋")
    
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())