import random
import string
import asyncio
import python_weather
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
    
    # Проверяем, указана ли длина пароля
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
        
    # Функция генерации пароля
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
    # Список всех команд бота
    await message.answer(
        "Команды:\n"
        "/start - Приветствие\n"
        "/help - Список команд\n"
        "/password [число] — любая длина (по умолчанию 8)\n"
        "/weather [город] [дней]"
    )
    
# ====================
# help comands

# ====================
# weather start
# Словарь перевода погоды на русский
weather_translations = {
    'Partly Cloudy': 'Переменная облачность',
    'Clear': 'Ясно',
    'Sunny': 'Солнечно',
    'Cloudy': 'Облачно',
    'Overcast': 'Пасмурно',
    'Rain': 'Дождь',
    'Light Rain': 'Небольшой дождь',
    'Moderate Rain': 'Умеренный дождь',
    'Heavy Rain': 'Сильный дождь',
    'Light rain shower': 'Легкий дождь',
    'Rain shower': 'Дождь',
    'Snow': 'Снег',
    'Light Snow': 'Небольшой снег',
    'Heavy Snow': 'Сильный снег',
    'Thunderstorm': 'Гроза',
    'Fog': 'Туман',
    'Mist': 'Дымка',
    'Drizzle': 'Морось',
    'Showers': 'Ливень',
    'Patchy rain': 'Местами дождь',
    'Patchy snow': 'Местами снег',
    'Patchy sleet': 'Местами мокрый снег',
    'Blizzard': 'Метель',
    'Freezing rain': 'Ледяной дождь',
    'Hail': 'Град',
    'Fair': 'Ясно',
    'Mostly Cloudy': 'Облачно с прояснениями',
    'Partly cloudy': 'Переменная облачность',
    'Scattered clouds': 'Рассеянные облака',
    'Broken clouds': 'Разорванная облачность',
    'Few clouds': 'Малооблачно',
    'Patchy rain nearby': 'Местами дождь поблизости'
}

@dp.message(Command("weather"))
async def handle_weather(message: Message):
    args = message.text.split()
    
    # Проверяем, что есть город
    if len(args) < 2:
        await message.answer("❌ Укажи город")
        return
        
    city = args[1]
    days = 1
    

    # Проверяем, указано ли количество дней
    if len(args) > 2:
        try:
            days = int(args[2])
            if days < 1:
                await message.answer("❌ Дней должно быть больше 0!")
                return
            if days > 7:
                await message.answer("❌ Максимум 7 дней!")
                return
        except ValueError:
            await message.answer("Укажи число дней, например: /weather Москва 5")
    try:
        # Подключаемся к API погоды
        async with python_weather.Client() as client:
            weather = await client.get(city)
            
            if weather is None:
                await message.answer(f"❌ Город '{city}' не найден!")
                return
        # Прогноз на текущий день
        if days == 1:
            description_ru = weather_translations.get(weather.description, weather.description)
            await message.answer(
                f"🌤 **Погода в {city}:**\n"
                f"🌡 Температура: {weather.temperature}°C\n"
                f"☁️ Погода: {description_ru}\n"
                f"💧 Влажность: {weather.humidity}%\n"
                f"💨 Ветер: {weather.wind_speed} км/ч"
            )
        else:
            # Прогноз на несколько дней
            forecast = f"📅 **Прогноз погоды в {city} на {days} дней**\n\n"
            
            daily_forecasts = []
            for i, daily in enumerate(weather.daily_forecasts[:days]):
                date = daily.date.strftime("%d.%m")
                descrip_ru = weather_translations.get(daily.description, daily.description)
            
                forecast += (
                    f"📆 {date}:\n"
                    f"🌡 Температура: {daily.temperature}°C\n"
                    f"☁️ {descrip_ru}\n"
                    f"💧 Влажность: {daily.humidity}%\n"
                    f"💨 Ветер: {daily.wind_speed} км/ч"
                )
            await message.answer(forecast)
            
    except Exception as e:
        await message.answer(f"❌ Ошибка: не удалось получить погоду. Попробуй позже.")


# ====================
# weather stop

async def main():
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
     # Запускаем асинхронную функцию main
    asyncio.run(main())