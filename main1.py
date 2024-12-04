import asyncio
import logging
from gc import callbacks
from turtledemo.penrose import start
from xml.sax import parse

from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
import json
import random
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
# Импортируем модуль random для генерации случайных чисел
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


# Функция для сохранения конфигурации в JSON-файл
def save_config(file_path):
    global config
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


# Функции для работы с данными пользователей
# Функция для увеличения количества правильных ответов
def update_correct_count(chat_id):
    global config

    # Проверяем, существует ли пользователь в конфигурации
    if str(chat_id) not in config["users"]:
        config["users"][str(chat_id)] = {"correct_count": 0, "level": 0}  # создаем нового пользователя

    config["users"][str(chat_id)]["correct_count"] += 1  # Увеличиваем количество правильных ответов
    save_config('config.json')  # Сохраняем изменения в config.json


# Функции для работы с данными пользователей
def update_level(chat_id, level):
    global config
    user_id_str = str(chat_id)

    # Проверяем, существует ли пользователь в конфигурации
    if user_id_str not in config["users"]:
        config["users"][user_id_str] = {"correct_count": 0, "level": 0}  # создаем нового пользователя

    # Устанавливаем уровень пользователя
    config["users"][user_id_str]['level'] = level

    save_config('config.json')  # Сохраняем изменения в config.json
    return config["users"][user_id_str]['level']


def get_correct_count(chat_id):
    global config
    return config["users"][str(chat_id)]["correct_count"]


def reset(chat_id):
    config["users"][str(chat_id)]["correct_count"] = 0
    save_config('config.json')  # Сохраняем изменения в config.json


# Загрузка конфигурации
config = load_config('config.json')
bot = Bot(config['BOT_TOKEN'])

dp = Dispatcher()
router = Router()  # Создаем экземпляр Router


async def level_1_alg(mess: types.message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(1, 10)  # Случайное число от 1 до 10
    num2 = random.randint(1, 10)  # Случайное число от 1 до 10

    # Формируем задачу как строку
    primer = f"{num1} + {num2}"
    otvet = num1 + num2  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())

async def level_2_alg(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(1, 10)  # Случайное число от 1 до 10
    num2 = random.randint(1, 10)  # Случайное число от 1 до 10

    # Формируем задачу как строку
    if num1 > num2:
        primer = f"{num1} - {num2}"
        otvet = num1 - num2  # Правильный ответ
    else:
        primer = f"{num2} - {num1}"
        otvet = num2 - num1  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())

async def level_3_alg(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(1, 10)  # Случайное число от 1 до 10
    num2 = random.randint(1, 10)  # Случайное число от 1 до 10
    num3 = random.randint(1, 10)  # Случайное число от 1 до 10
    operator = ['+', '-']
    values = [num1, random.choice(operator), num2, random.choice(operator), num3]

    # Формируем задачу как строку
    primer = f"{' '.join(map(str, values))}"
    if values[1] == '+' and values[3] == '+':
        otvet = num1 + num2 + num3  # Правильный ответ
    elif values[1] == '-' and values[3] == '+':
        otvet = num1 - num2 + num3  # Правильный ответ
    elif values[1] == '-' and values[3] == '-':
        otvet = num1 - num2 - num3  # Правильный ответ
    else:
        otvet = num1 + num2 - num3  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())

async def level_4_alg(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(1, 10)  # Случайное число от 1 до 10
    num2 = 'X'  # Случайное число от 1 до 10
    num3 = random.randint(1, 10)  # Случайное число от 1 до 10
    num4 = '='
    operator = ['+', '-']
    values = [num1, random.choice(operator), num2, num4, num3]

    # Формируем задачу как строку
    primer = f"{' '.join(map(str, values))}"
    if values[1] == '+':
        otvet = num3 - num1  # Правильный ответ
    else:
        otvet = -1 * (num3 - num1)  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())

async def level_5_alg(mess: types.Message, state: FSMContext):
    # Генерация двух случайных чисел
    num1 = random.randint(2, 9)  # Случайное число от 2 до 9
    num2 = random.randint(2, 9)  # Случайное число от 2 до 9

    # Формируем задачу как строку
    primer = f"{num1} * {num2}"
    otvet = num1 * num2  # Правильный ответ

    await mess.answer(primer)  # Отправка примера пользователю

    await state.update_data(correct=otvet)  # Сохраняем правильный ответ в состоянии
    await state.set_state(GameStates.waiting_for_answer)  # Переход в состояние ожидания ответа

    # Удаляем клавиатуру с кнопкой "Начать"
    await mess.answer("Напишите ваш ответ:", reply_markup=ReplyKeyboardRemove())

async def nest_ex(mess: types.Message, state: FSMContext):
    if config["users"][str(mess.chat.id)]['level'] == 1:
        await level_1_alg(mess, state)
    elif config["users"][str(mess.chat.id)]['level'] == 2:
        await level_2_alg(mess, state)
    elif config["users"][str(mess.chat.id)]['level'] == 3:
        await level_3_alg(mess, state)
    elif config["users"][str(mess.chat.id)]['level'] == 4:
        await level_4_alg(mess, state)
    elif config["users"][str(mess.chat.id)]['level'] == 5:
        await level_5_alg(mess, state)

# Обработчик команды "/start"
@dp.message(CommandStart())
async def handle_start(mess: types.Message):
    # Создание кнопки "Начать"
    start_button = KeyboardButton(text="Меню")

    # Создание разметки клавиатуры
    markup = ReplyKeyboardMarkup(
        keyboard=[[start_button]],  # Кнопка обернута в список
        resize_keyboard=True
    )

    await mess.answer(text=f"Привет, {mess.from_user.full_name}👋 \nГотов решать примеры?\nTогда перейди в меню⬇️",
                      reply_markup=markup)


# Создание кнопок
@dp.message(lambda message: message.text in ['Меню', '/menu'])
async def vibor_knopok(mess: types.Message):
    # Создание кнопок
    button1 = KeyboardButton(text='1 Уровень')
    button2 = KeyboardButton(text='2 Уровень')
    button3 = KeyboardButton(text='3 Уровень')
    button4 = KeyboardButton(text='4 Уровень')
    button5 = KeyboardButton(text='5 Уровень')

    markup4 = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2], [button3], [button4], [button5]],  # Кнопка обернута в список
        resize_keyboard=True
    )
    discription = '''<b>Выберите уровень:</b>

<b>1 Уровень</b> - сложение чисел до десяти
<b>2 Уровень</b> - вычитание чисел до десяти
<b>3 Уровень</b> - примры с тремя числами
<b>4 Уровень</b> - уровнения
<b>5 Уровень</b> - умножение

Пользуйтесь клавиатурой ниже⬇️'''
    await mess.answer(discription, reply_markup=markup4, parse_mode='HTML')


# Обработка кнопки 1 уровня
@dp.message(lambda message: message.text in ["1 Уровень"])
async def level_1(mess: types.Message, state: FSMContext):
    update_level(mess.chat.id, 1)
    await level_1_alg(mess, state)


# Обработка кнопки 2 уровня
@dp.message(lambda message: message.text == "2 Уровень")
async def level_2(mess: types.Message, state: FSMContext):
    update_level(mess.chat.id, 2)
    await level_2_alg(mess, state)


# Обработка кнопки 3 уровня
@dp.message(lambda message: message.text == "3 Уровень")
async def level_3(mess: types.Message, state: FSMContext):
    update_level(mess.chat.id, 3)
    await level_3_alg(mess, state)


# Обработка кнопки 4 уровня
@dp.message(lambda message: message.text == "4 Уровень")
async def level_4(mess: types.Message, state: FSMContext):
    update_level(mess.chat.id, 4)
    await level_4_alg(mess, state)


# Обработка кнопки 5 уровня
@dp.message(lambda message: message.text == "5 Уровень")
async def level_5(mess: types.Message, state: FSMContext):
    update_level(mess.chat.id, 5)
    await level_5_alg(mess, state)


def random_fraze(fraz):
    return random.choice(fraz)


items = ['Верно Ты молодец 👍', 'Так держать!Попробуй ещё!', 'Крассавчик! Давай ещё раз!', 'Ты меня приятно удевляешь🤗']
items2 = ['Неверно.', 'К сожаленеию ты ошибся 😥']


def random_stiker(stiker):
    return random.choice(stiker)


punkt1 = ['CAACAgIAAxkBAAENFSxnLEWJllFn6GWjQZpSKakkXjjuBQACO2AAAumkYUnpQOyMecsdKjYE',
          'CAACAgIAAxkBAAENFTBnLEWWnkvyyTzbmwcnSGTPpK9QPQACOFwAAiyQYEm4Eyn0CW_8hjYE',
          'CAACAgIAAxkBAAENFYZnLPiImlW2qCdvaVRPE8lz4RUc-wACbFsAAjyaYUl-YMD5EipofTYE',
          'CAACAgIAAxkBAAENPP9nSLcPF3oH0CdjTGyP5hK8cL92EwACWmMAAkwHSUrnAUqBfkECiDYE']
punkt2 = ['CAACAgIAAxkBAAENFYhnLPiOM2yswTHAWKKPEE1CZSO_JQACpmMAAkWOYUkkQ0QyiWQJtjYE',
          'CAACAgIAAxkBAAENFTJnLEWcNuYbJpXsZVafEW1SZrsekgACQmIAAvqMYEnL2hH1A6GdeDYE']


# Дальнейшая логика для обработки ответа от пользователя
@dp.message(GameStates.waiting_for_answer)
async def send_otvet(mess: types.Message, state: FSMContext):
    chat_id = mess.chat.id
    user_data = await state.get_data()
    correct_answer = user_data['correct']
    # Не числовой ответ
    if not mess.text.lstrip('-').isdigit():
        await bot.send_sticker(chat_id=mess.from_user.id,
                               sticker=r"CAACAgIAAxkBAAENFS5nLEWPuXkFlcRm46H_Bbi61O0INQACsF0AArkDWUlb0TBPfS4f6DYE")
        await mess.answer("Пожалуйста, введите числовой ответ.")

    # Правильный ответ
    elif int(mess.text) == correct_answer:
        update_correct_count(chat_id)  # Обновить количество правильных ответов
        current_count = get_correct_count(chat_id)  # Получить текущее количество
        # button1 = InlineKeyboardButton(text='Решать ещё', callback_data='button1')
        # button2 = InlineKeyboardButton(text='Перейти в меню', callback_data='bu2')
        # keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1],[button2]])
        await bot.send_sticker(chat_id=mess.from_user.id,
                               sticker=random_stiker(punkt1))
        await mess.answer(random_fraze(items))  # , reply_markup=keyboard)

        if current_count == 7:
            reset(chat_id)
            await bot.send_sticker(chat_id=mess.from_user.id,
                                   sticker='CAACAgIAAxkBAAENJC9nOg2xtFaEWflZn3VHxelVqXU0wQACx1wAAi3g0UkMS28Cja1oYzYE')
            button4 = InlineKeyboardButton(text='Перейти на следующий уровнь', call
                                           back_data='bu2')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button4]])
            await mess.answer('Молодец! Ты ответил правильно 7 раз подряд!\nПереходи на следующий уровнь',
                              reply_markup=keyboard)
        else:
            await state.set_state(None)  # Завершаем состояние
            await nest_ex(mess, state)

    # Не правильный ответ
    else:
        await bot.send_sticker(chat_id=mess.from_user.id,
                               sticker=random_stiker(punkt2))
        await mess.answer(
            f'{random_fraze(items2)}\nПравильный ответ был: {correct_answer}.')  # , reply_markup=keyboard)
        await state.set_state(None)  # Завершаем состояние
        await nest_ex(mess, state)



@router.callback_query(lambda c: c.data in ['bu2'])
async def process_callback_button1(callback_query: types.CallbackQuery):
    # Создание кнопок
    button1 = KeyboardButton(text='1 Уровень')
    button2 = KeyboardButton(text='2 Уровень')
    button3 = KeyboardButton(text='3 Уровень')
    button4 = KeyboardButton(text='4 Уровень')
    button5 = KeyboardButton(text='5 Уровень')

    markup4 = ReplyKeyboardMarkup(
        keyboard=[[button1], [button2], [button3], [button4], [button5]],  # Кнопка обернута в список
        resize_keyboard=True
    )
    discription = '''<b>Выберите уровень:</b>

    <b>1 Уровень</b> - сложение чисел до десяти
    <b>2 Уровень</b> - вычитание чисел до десяти
    <b>3 Уровень</b> - примры с тремя числами
    <b>4 Уровень</b> - неравенства
    <b>5 Уровень</b> - уровнения
    <b>6 Уровень</b> - умножение

    Пользуйтесь клавиатурой ниже⬇️'''
    await callback_query.message.answer(discription, reply_markup=markup4, parse_mode='HTML')


# Основная асинхронная функция программы
async def main():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router)  # Регистрация Router в Dispatcher
    await dp.start_polling(bot)


# Запуск основного асинхронного процесса
if __name__ == '__main__':
    asyncio.run(main())
