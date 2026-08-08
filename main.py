import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector

BOT_TOKEN = "8992122596:AAFZkWeWXeIqGRG6U_MwDspVjTQ1n7ES0Hc"

# Бесплатные публичные прокси (могут работать нестабильно, но для теста ок)
PROXY_LIST = [
    'socks5://45.136.244.17:1080',
    'socks5://46.8.28.35:1080',
    'socks5://46.8.29.19:1080',
    'socks5://85.203.17.66:1080',
    'http://45.136.244.17:8080',
]

def get_proxy():
    # Берем первый рабочий прокси из списка
    for proxy in PROXY_LIST:
        try:
            return ProxyConnector.from_url(proxy)
        except:
            continue
    return None

proxy_connector = get_proxy()
if proxy_connector:
    session = AiohttpSession(connector=proxy_connector)
    bot = Bot(token=BOT_TOKEN, session=session)
else:
    bot = Bot(token=BOT_TOKEN)  # fallback без прокси

dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет! Я бот-помощник 👋")
    
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())