from keyboards import reply as rkb, inline as ikb
from misc import util, database as db
from config import logger, get_conn
from ai import connection as AI
from assets import texts as txt
from create_bot import dp, bot
from datetime import datetime
from tools import MainMessage
from aiogram import types


@logger.catch
async def start_bot(message: types.Message):
	"""
	/start command
	"""
	USER_ID = message["from"]["id"]

	await message.answer(txt.greeting, reply_markup=rkb.base)
	
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
		"visit_time": current_time.strftime("%H:%M:%S"),
		"ai_model": "text-davinci-003"
	}

	added = db.add_user(connection, cursor, user_data)

	if not added:
		logger.error(f"{USER_ID}: {added=}")


@logger.catch
async def ai_model_choice(message: types.Message):
	"""
	Sends message with ikg.models markup to choose ai model
	"""
	msg = await message.answer(txt.ai_model_choice, reply_markup=ikb.ai_models)
	await MainMessage.acquire(msg)


# PROMPTS INPPUT


@logger.catch
async def general(message: types.Message):
	USER_ID = message["from"]["id"]
	prompt = message["text"]

	options = {
		"text-davinci-003": answer_chat,
		"image-alpha-001": answer_image
	}

	connection = get_conn()
	cursor = connection.cursor()

	ai_model = db.get_ai_model(cursor, USER_ID)

	cursor.close()
	connection.close()

	if not ai_model:
		await message.answer(txt.error_message)
		return

	response = await AI.Response(ai_model, prompt).get()
	await options[ai_model](USER_ID, response)


@logger.catch
async def answer_chat(USER_ID: int, message: str):
	"""
	Sends msg ansmwer to user
	"""
	await util.send_long_message(USER_ID, message)


@logger.catch
async def answer_image(USER_ID: int, url: str):
	"""
	Sends image to user by url
	"""
	await bot.send_photo(USER_ID, url) #, caption=url