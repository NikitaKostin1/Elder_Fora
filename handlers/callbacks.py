from config import logger, get_conn
from misc import util, database as db
from assets import texts as txt
from create_bot import dp, bot
from tools import MainMessage
from aiogram import types


@logger.catch
async def set_ai_model(callback: types.CallbackQuery):
	USER_ID = callback["message"]["chat"]["id"]
	model = callback.data.split()[1]

	await callback.answer()

	connection = get_conn()
	cursor = connection.cursor()

	saved = db.set_ai_model(connection, cursor, USER_ID, model)

	cursor.close()
	connection.close()

	if not saved:
		await callback.message.answer("Не удалось")
		return

	await MainMessage.edit(USER_ID, text=txt.models_tips[model])

