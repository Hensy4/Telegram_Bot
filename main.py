import random
import string
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

BOT_TOKEN = "8992122596:AAFZkWeWXeIqGRG6U_MwDspVjTQ1n7ES0Hc"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ====================
# password start



@dp.message(Command("password"))
async def handle_password(message: Message):
    args = message.text.split()
    length = 8
    
    if len(args) > 1:
        try:
            length = int(args[1])
            if length < 4:
                await message.answer("Пароль должен быть длиннее 4 символов!")
                return
            if length > 100:
                await message.answer("Слишком длинный пароль (максимум 100)")
                return
        except ValueError:
            await message.answer("Укажи число, например: /password 20")
            return
        
  
    def generate(length):
        all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + "!@#$%^&*()_+-="
        _password = ''.join(random.choice(all_chars) for _ in range(length))
        return _password
    
    await message.answer(f"Твой пароль: {generate(length)}")

# ====================
# password stop 


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Я бот-помощник 👋")
    
# ====================
# help comands
    
@dp.message(Command("help"))
async def handle_help(message: Message):
    await message.answer(
        "Команды:\n"
        "/start - Приветствие\n"
        "/help - Список команд\n"
        "/password [число] — любая длина (по умолчанию 8)\n"
        
    )
    
# ====================
# help comands

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())