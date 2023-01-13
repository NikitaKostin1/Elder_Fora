from misc import util, database as db
from config import logger, get_conn
from ai import connection as AI
from create_bot import dp, bot
from datetime import datetime
from aiogram import types


@logger.catch
async def start_bot(message: types.Message):
	"""
	/start command
	"""
	USER_ID = message["from"]["id"]

	await message.answer("👋")
	
	connection = get_conn()
	cursor = connection.cursor()

	user_exists = db.user_exists(cursor, USER_ID)

	if user_exists:
		cursor.close()
		connection.close()
		return

	current_time = datetime.now()

	user_data = {
		"user_id": USER_ID,
		"username": message["from"]["username"],
		"visit_date": current_time.strftime("%Y-%m-%d"),
		"visit_time": current_time.strftime("%H:%M:%S")
	}

	added = db.add_user(connection, cursor, user_data)

	if not added:
		logger.error(f"{USER_ID}: {added=}")








@logger.catch
async def general(message: types.Message):
	USER_ID = message["from"]["id"]
	prompt = message["text"]
	
	response = await AI.get_response(prompt)
	await util.send_long_message(USER_ID, response)
