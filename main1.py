import asyncio
import logging
from gc import callbacks
from turtledemo.penrose import start
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
import json
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import random  # Импортируем модуль random для генерации случайных чисел
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router


class GameStates(StatesGroup):
    waiting_for_answer = State()


# Функция для загрузки конфигурации из JSON-файла
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Загрузка конфигурации
config = load_config('config.json')
bot = Bot(config['BOT_TOKEN'])

dp = Dispatcher()
router = Router()  # Создаем экземпляр Router


# Обработчик команды "/start"
@dp.message(CommandStart())
async def handle_start(mess: types.Message):
    # Создание кнопки "Начать"
    start_button = KeyboardButton(text="Конечно")

    # Создание разметки клавиатуры
    markup = ReplyKeyboardMarkup(
        keyboard=[[start_button]],  # Кнопка обернута в список
        resize_keyboard=True
    )

    await mess.answer(text=f"Привет, {mess.from_user.full_name}! Готов решать примеры?", reply_markup=markup)


# Создание кнопок
@dp.message(lambda message: message.text == "Конечно")
async def vibor_knopok(mess: types.Message):
    # Создание кнопок
    button1 = KeyboardButton(text='Сложение')
    button2 = KeyboardButton(text='Вычитание')
    button3 = KeyboardButton(text='Умножение')

    markup4 = ReplyKeyboardMarkup(
        keyboard=[[button1],[button2],[button3]],  # Кнопка обернута в список
        resize_keyboard=True
    )
    await mess.answer(text=f"Тогда выбери вариант примеров!", reply_markup=markup4)


# Обработчик команды "Сложение"
@dp.message(lambda message: message.text == "Сложение")
async def sloshenie(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(1, 20)  # Случайное число от 1 до 20
    num2 = random.randint(1, 20)  # Случайное число от 1 до 20

    # Формируем задачу как строку
    primer = f"{num1} + {num2}"
    otvet = num1 + num2  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())


# Обработчик команды "Вычитание"
@dp.message(lambda message: message.text == "Вычитание")
async def vchitanie(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(10, 20)  # Случайное число от 10 до 20
    num2 = random.randint(1, 9)  # Случайное число от 1 до 9

    # Формируем задачу как строку
    primer = f"{num1} - {num2}"
    otvet = num1 - num2  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())


# Обработчик команды "Умножение"
@dp.message(lambda message: message.text == "Умножение")
async def umnocenie(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(1, 10)  # Случайное число от 1 до 9
    num2 = random.randint(1, 10)  # Случайное число от 1 до 9

    # Формируем задачу как строку
    primer = f"{num1} * {num2}"
    otvet = num1 * num2  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())


# Дальнейшая логика для обработки ответа от пользователя
@dp.message(GameStates.waiting_for_answer)
async def send_otvet(mess: types.Message, state: FSMContext):
    user_data = await state.get_data()  # Получаем данные состояния
    correct_answer = user_data['correct']  # Получаем правильный ответ

    # Проверяем, правильно ли ответил пользователь
    if not mess.text.isdigit():
        await mess.answer("Пожалуйста, введите числовой ответ.")
    elif int(mess.text) == correct_answer:
        # Создаем клавиатуру
        button1 = InlineKeyboardButton(text='Решать ещё', callback_data='button1')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1]])
        #keyboard.add(button1)

        await mess.answer("Правильно!", reply_markup=keyboard)
    else:
        # Создаем клавиатуру
        button2 = InlineKeyboardButton(text='Решать ещё', callback_data='button2')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button2]])
        await mess.answer(f'Неправильно. Правильный ответ был {correct_answer}. Попробуй заново.',reply_markup=keyboard)

    await state.set_state(None)  # Завершаем состояние


# Обработчик для кнопки "Решать ещё"
@router.callback_query(lambda c: c.data in ['button1','button2'] )
async def process_callback_button1(callback_query: types.CallbackQuery):
    button1 = KeyboardButton(text='Сложение')
    button2 = KeyboardButton(text='Вычитание')
    button3 = KeyboardButton(text='Умножение')

    markup4 = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2], [button3]],
        resize_keyboard=True
    )
    print(callback_query.message.from_user)
    await callback_query.message.answer(text="Тогда выбери вариант примеров!", reply_markup=markup4)


# Основная асинхронная функция программы
async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)  # Регистрация Router в Dispatcher
    await dp.start_polling(bot)


# Запуск основного асинхронного процесса
if __name__ == '__main__':
    asyncio.run(main())
