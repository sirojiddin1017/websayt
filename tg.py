from aiogram import types, Bot, Dispatcher
from aiogram.filters import Command
import asyncio
from random import randint

TOKEN = "8048073971:AAFlheWO4HLnmov97Shk6SYaQV2mMtuB_pQ"

ChannelName = ""

bot = Bot(token=TOKEN)

dp = Dispatcher()

user_data = {}


@dp.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data or message.text == "/start":
        await start(message)
    elif "phone" not in user_data[user_id]:
        await ask_phone(message)
    elif "status" not in user_data[user_id]:
        await check_code(message)
    elif "location" not in user_data[user_id]:
        await info_location(message)
    elif "kategoriyalar" in user_data[user_id]["holat"]:
        await show_city(message)


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    button = [
        [types.KeyboardButton(text="Raqam jo'natish", request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer("Assalomu aleykum! Les Ailes yetkazib berish xizmatiga xush kelibsiz.", reply_markup=keyboard)
    print(user_data)


async def ask_phone(message: types.Message):
    user_id = message.from_user.id
    i = '+1234567890'
    ok = True
    if message.contact is not None:
        phone_c = message.contact.phone_number
        user_data[user_id]['phone'] = phone_c
        ver_code = randint(100000, 999999)
        user_data[user_id]['ver_code'] = ver_code
        await message.answer(f"Nomeringizga tasdiqlash kodi yuborildi \nIltimos kodni kiriting: {ver_code}")
    elif len(message.text) == 13 and message.text[0:4] == '+998':
        for symbol in message.text:
            if symbol not in i:
                await message.answer('Hato nomer kiritildi')
                ok = False
                break
        if ok == True:
            phone = message.text
            user_data[user_id]['phone'] = phone
            ver_code = randint(100000, 999999)
            user_data[user_id]['ver_code'] = ver_code
            await message.answer(f"Nomeringizga tasdiqlash kodi yuborildi \nIltimos kodni kiriting: {ver_code}")

    else:
        await message.answer('Hato nomer kiritildi')
        print(user_data)


async def check_code(message: types.Message):
    user_id = message.from_user.id
    code = message.text
    ver_code = user_data[user_id]["ver_code"]
    if str(ver_code) == code:
        user_data[user_id]["status"] = "verified"
        await message.answer("Nomeringiz tasdiqlandi")
        await ask_location(message)
    else:
        await message.answer("Kod xato terildi. Yana urinib ko'ring")
    print(user_data)


async def ask_location(message: types.Message):
    user_id = message.from_user.id
    button = [
        [types.KeyboardButton(text="Lokatsiya jo'natish", request_location=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer("Lokatsiyani jo'nating", reply_markup=keyboard)
    print(user_data)
    async def info_location(message: types.Message):
    user_id = message.from_user.id
    if message.location is not None:
        latitude = message.location.latitude
        longitude = message.location.longitude
        location = {
            "latitude": latitude,
            "longitude": longitude
        }
    else:
        location = message.text
    user_data[user_id]["location"] = location
    button = [
        [types.KeyboardButton(text="Boshlash")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    user_data[user_id]["holat"] = "kategoriyalar"
    await message.answer("Boshladikmi", reply_markup=keyboard)
    print(user_data)


city = [
    "Toshkent", "Andijon",
    "Samarqand", "Farg'ona",
    "Buxoro", "Marg'ilon",
    "Nukus", "Xorazm",
    "Chirchiq"
]

