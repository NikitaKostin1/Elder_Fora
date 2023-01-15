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
	username = message["from"]["username"]

	await message.answer(txt.greeting, reply_markup=rkb.base)
	await bot.send_message(381906725, txt.admin_user_untered.format(USER_ID=USER_ID, username=username))

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
		"username": username,
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

	model_options = {
		"text-davinci-003": {"response": answer_chat, "action": "typing"},
		"image-alpha-001": {"response": answer_image, "action": "upload_photo"}
	}

	connection = get_conn()
	cursor = connection.cursor()

	ai_model = db.get_ai_model(cursor, USER_ID)

	cursor.close()
	connection.close()

	if not ai_model:
		await message.answer(txt.error_message)
		return

	await message.answer_chat_action(model_options[ai_model]["action"])

	response = await AI.Response(ai_model, prompt).get()
	await model_options[ai_model]["response"](USER_ID, response)


@logger.catch
async def answer_chat(USER_ID: int, message: str):
	"""
	Sends msg ansmwer to user
	"""
	if not message:
		await bot.send_message(USER_ID, "Слишком сложный запрос ;(")
		return

	await util.send_long_message(USER_ID, message)


@logger.catch
async def answer_image(USER_ID: int, url: str):
	"""
	Sends image to user by url
	"""
	if not url:
		await bot.send_message(USER_ID, "Слишком сложный запрос ;(")
		return

	await bot.send_photo(USER_ID, url) #, caption=url