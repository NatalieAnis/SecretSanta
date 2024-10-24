# @hsesecretsanta_bot
from pyexpat.errors import messages

import aiogram
import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from colorama import init, Style

init(autoreset=True)


def print_bold(text):
    return f"{Style.BRIGHT}{text}"


logging.basicConfig(level=logging.INFO)
bot = Bot(token='7922973655:AAGKSoXtt49RQYfq14lDE5HHdp6vgBwRJ2M')
dp = Dispatcher()
router = Router()


@router.message(Command('start'))
async def send_welcome(message: Message):
    kb = [
        [
            types.KeyboardButton(text="создать новую комнату"),
            types.KeyboardButton(text="приступить к игре: отправить трек-номер"),
            types.KeyboardButton(text="правила игры")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb
    )
    username = message.from_user.username
    await message.answer('Хо-хо-хо, приятной игры, ' + username + '' + "🎲", reply_markup=keyboard)


@router.message(F.text.lower() == 'правила игры')
async def game_rules(message: Message):
    rules_message = (
        f"{print_bold('Правила игры:')}\n"
        "Тайный Санта — это традиционная новогодняя игра, в которой участники обмениваются подарками, оставаясь при этом анонимными. "
        "Обычно ограничивается бюджет на подарок и устанавливается дата обмена сюрпризами. "
        "Важно сохранять конфиденциальность: никто не должен раскрывать, кто его 'Тайный Санта', до момента икс.\n\n"
        f"{print_bold('Чем я могу Вам помочь?')}\n"
        "Создавай новую комнату и добавляй туда своих друзей. У каждой комнаты есть свой уникальный трек-номер, "
        "благодаря которому вы сможете получить к ней доступ, узнать своего подопечного и прочитать его пожелания к подарку."
    )
    await message.answer(rules_message)


@router.message(F.text.lower() == 'создать новую комнату')
async def game_rules(message: Message):
    import string
    import secrets
    def room_number(file_room_number):
        letters_and_digits = string.ascii_letters + string.digits
        track_number = ''.join(secrets.choice(letters_and_digits) for i in range(10))

        with open(file_room_number, 'a+') as f:
            f.seek(0)
            if track_number not in f.read():
                f.write(track_number + '\n')
                return track_number
            else:
                return room_number(file_room_number)

    file_name = 'room_numbers.txt'
    await message.answer('Уникальный трек-номер вашей комнаты: ' + room_number(file_name))
    await message.answer(
        'Пожайлуста, добавте в комнату участников, записав их ники в телеграмме. В формате:\n dobrisanta\n lolkek\n oleniha')


result = {}


@router.message(F.text.lower() == 'приступить к игре: отправить трек-номер')
async def game_start(message: Message):
    await message.answer('Отправь свой трек-номер.')


import os


def read_room_numbers(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read().splitlines()
        return {}


room_numbers = read_room_numbers('room_numbers.txt')


@router.message(lambda message: message.text in room_numbers)
async def repeat_text(password: Message):
    username = password.from_user.username
    await password.answer(username + ", " + "добро пожаловать в комнату " + password.text)
    if result[password.from_user.id]:
        await password.answer(f"{username}, твой тайный санта - это {result[password.from_user.id][username]}.")

    @router.message(F.text)
    async def players_add(friends: Message):
        await friends.reply('Все участники успешно добавлены в комнату. Теперь вы можете приступить к игре!')
        list_friends = friends.text.split()
        import random
        def mix(list_friends):
            if len(list_friends) < 2:
                raise ValueError
            santa_list = list_friends.copy()
            random.shuffle(santa_list)
            assignments = {}
            for i in range(len(list_friends)):
                santa = list_friends[i]
                receiver = santa_list[i]
                if santa == receiver:
                    return mix(list_friends)
                assignments[santa] = receiver

        result[friends.from_user.id] = mix(list_friends)
        await friends.reply

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())