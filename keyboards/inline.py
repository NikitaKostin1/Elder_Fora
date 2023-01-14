from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ai_models = InlineKeyboardMarkup(row_width=2)
b1 = InlineKeyboardButton(text="Чат 💭", callback_data="ai_model text-davinci-003")
b2 = InlineKeyboardButton(text="Генерация картинок 🏙", callback_data="ai_model image-alpha-001")
ai_models.add(b1).add(b2)