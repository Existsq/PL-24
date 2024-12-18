import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from transitions import Machine
from os import getenv
import psycopg2
from datetime import datetime

# Установим параметры для PostgreSQL
DB_NAME = "pl"
DB_USER = "exist"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"

# Telegram API токен
API_TOKEN = getenv("BOT_TOKEN")


# Настройка бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Определяем состояния
states = ['START', 'COLLECTING_DATA', 'CONFIRMATION']

# Переходы между состояниями
transitions = [
    {'trigger': 'start_booking', 'source': 'START', 'dest': 'COLLECTING_DATA'},
    {'trigger': 'collect_data', 'source': 'COLLECTING_DATA', 'dest': 'CONFIRMATION'},
    {'trigger': 'confirm_booking', 'source': 'CONFIRMATION', 'dest': 'START'},
]

# Класс для управления состояниями и данными
class BookingStateMachine:
    def __init__(self):
        self.machine = Machine(model=self, states=states, transitions=transitions, initial='START')
        self.user_data = {}


bot_state = BookingStateMachine()


# Подключение к базе данных
def db_connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    bot_state.start_booking()
    await message.reply("Добро пожаловать! Начнем бронирование. Сколько человек будет на бронировании?")


# Обработчик для сбора данных
@dp.message(lambda message: bot_state.state == 'COLLECTING_DATA')
async def collect_data_handler(message: Message):
    if 'num_people' not in bot_state.user_data:
        bot_state.user_data['num_people'] = int(message.text)
        await message.reply("Введите время бронирования (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
    else:
        try:
            bot_state.user_data['reservation_time'] = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
            bot_state.collect_data()
            await message.reply(
                f"Вы хотите забронировать столик на {bot_state.user_data['num_people']} человек в "
                f"{bot_state.user_data['reservation_time']}. Подтверждаете? (да/нет)"
            )
        except ValueError:
            await message.reply("Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД ЧЧ:ММ.")


# Обработчик подтверждения бронирования
@dp.message(lambda message: bot_state.state == 'CONFIRMATION')
async def confirm_booking_handler(message: Message):
    if message.text.lower() == 'да':
        # Подтверждаем бронирование и сохраняем в БД
        with db_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO reservations (user_id, num_people, reservation_time, confirmed) VALUES (%s, %s, %s, %s)",
                    (message.from_user.id, bot_state.user_data['num_people'], bot_state.user_data['reservation_time'],
                     True)
                )
                conn.commit()
        await message.reply("Ваше бронирование подтверждено! Спасибо!")
    else:
        await message.reply("Бронирование отменено.")

    # Сбрасываем состояние и данные
    bot_state.confirm_booking()
    bot_state.user_data.clear()


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
