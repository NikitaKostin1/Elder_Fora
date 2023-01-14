from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

base = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
b1 = KeyboardButton("Режим ⚙️")
base.add(b1)
