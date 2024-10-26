import asyncio
import logging
from turtledemo.penrose import start

from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
import json
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import random  # Импортируем модуль random для генерации случайных чисел
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


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

    try:
        # Проверяем, правильно ли ответил пользователь
        if int(mess.text) == correct_answer:
            await mess.answer("Правильно!")
        else:
            await mess.answer(f'Неправильно. Правильный ответ был {correct_answer}. Попробуй заново./start')
    except ValueError:
        await mess.answer("Пожалуйста, введите числовой ответ.")

    await state.set_state(None)  # Завершаем состояние


# Основная асинхронная функция программы
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


# Запуск основного асинхронного процесса
if __name__ == '__main__':
    asyncio.run(main())
