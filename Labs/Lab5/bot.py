import asyncio
import logging
import sys
import random
from os import getenv

import asyncpg
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# Получаем токен бота и данные для подключения к БД
TOKEN = getenv("BOT_TOKEN")
DATABASE_URL = getenv("DATABASE_URL")

# Инициализируем диспетчер и подключение к БД
dp = Dispatcher()

# Заранее создаем задания по категориям
tasks = {
    "Физическая активность": [
        "Сделай 10 отжиманий 💪",
        "Пройди 5000 шагов 🚶‍♂️",
        "Сделай планку на 1 минуту ⏳"
    ],
    "Саморазвитие": [
        "Прочитай одну главу книги 📚",
        "Выучи 5 новых слов на иностранном языке 🌏",
        "Напиши свои цели на месяц 📃"
    ],
    "Социальные": [
        "Сделай комплимент кому-нибудь 😊",
        "Позвони другу и поговори с ним 📞",
        "Напиши сообщение старому знакомому 💬"
    ]
}


async def init_db():
    """
    Инициализация подключения к базе данных и создание таблицы, если её нет.
    """
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id BIGINT PRIMARY KEY,
            full_name TEXT,
            completed_tasks INT DEFAULT 0
        );
    ''')
    await conn.close()


async def update_user_stats(user_id: int, full_name: str):
    """
    Обновляет или добавляет запись пользователя, увеличивая счётчик выполненных заданий.
    """
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO user_stats (user_id, full_name, completed_tasks)
        VALUES ($1, $2, 1)
        ON CONFLICT (user_id)
        DO UPDATE SET completed_tasks = user_stats.completed_tasks + 1;
    ''', user_id, full_name)
    await conn.close()


async def get_user_rank(user_id: int):
    """
    Возвращает текущий рейтинг пользователя.
    """
    conn = await asyncpg.connect(DATABASE_URL)
    rank = await conn.fetchval('''
        SELECT COUNT(*) + 1 FROM user_stats
        WHERE completed_tasks > (SELECT completed_tasks FROM user_stats WHERE user_id = $1);
    ''', user_id)
    await conn.close()
    return rank


async def get_top_users(limit=10):
    """
    Возвращает топ пользователей по количеству выполненных заданий.
    """
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch('''
        SELECT full_name, completed_tasks FROM user_stats
        ORDER BY completed_tasks DESC LIMIT $1;
    ''', limit)
    await conn.close()
    return rows


def main_menu_keyboard():
    """
    Создает клавиатуру для главного меню с выбором категории и статистикой.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Физическая активность", callback_data="category_Физическая активность")],
        [InlineKeyboardButton(text="Саморазвитие", callback_data="category_Саморазвитие")],
        [InlineKeyboardButton(text="Социальные", callback_data="category_Социальные")],
        [InlineKeyboardButton(text="Мой рейтинг 🏅", callback_data="my_rank")],
        [InlineKeyboardButton(text="Топ пользователей 🏆", callback_data="top_users")]
    ])


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Приветствует пользователя и предлагает выбрать категорию задания.
    """
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Выберите категорию задания:",
                         reply_markup=main_menu_keyboard())


@dp.callback_query(lambda callback_query: callback_query.data.startswith("category_"))
async def category_task_callback(callback_query: CallbackQuery):
    """
    Обработчик для выбора категории и отправки задания.
    """
    category = callback_query.data.split("_")[1]
    task = random.choice(tasks[category])

    # Обновляем статистику пользователя
    await update_user_stats(callback_query.from_user.id, callback_query.from_user.full_name)

    # Клавиатура с опцией вернуться в главное меню
    task_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новое задание", callback_data=f"category_{category}")],
        [InlineKeyboardButton(text="Пропустить", callback_data=f"category_{category}")],
        [InlineKeyboardButton(text="Вернуться в главное меню", callback_data="main_menu")]
    ])

    await callback_query.message.answer(f"Твое задание по категории '{category}':\n{task}", reply_markup=task_keyboard)
    await callback_query.answer()


@dp.callback_query(lambda callback_query: callback_query.data == "my_rank")
async def my_rank_callback(callback_query: CallbackQuery):
    """
    Показывает текущий рейтинг пользователя.
    """
    rank = await get_user_rank(callback_query.from_user.id)
    await callback_query.message.answer(
        f"Твой текущий рейтинг: {rank}. Продолжай выполнять задания, чтобы повысить его! 🏅")
    await callback_query.answer()


@dp.callback_query(lambda callback_query: callback_query.data == "top_users")
async def top_users_callback(callback_query: CallbackQuery):
    """
    Показывает топ-10 пользователей по количеству выполненных заданий.
    """
    top_users = await get_top_users()
    top_text = "\n".join(
        [f"{idx + 1}. {user['full_name']} — {user['completed_tasks']} заданий" for idx, user in enumerate(top_users)])
    await callback_query.message.answer(f"🏆 Топ пользователей:\n\n{top_text}")
    await callback_query.answer()

@dp.callback_query(lambda callback_query: callback_query.data == "main_menu")
async def main_menu_callback(callback_query: CallbackQuery):
    """
    Обработчик для возврата в главное меню.
    """
    await callback_query.message.answer("Выберите категорию задания:", reply_markup=main_menu_keyboard())
    await callback_query.answer()


async def main() -> None:
    # Инициализация базы данных
    await init_db()

    # Инициализируем бота с HTML режимом для форматирования текста
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
