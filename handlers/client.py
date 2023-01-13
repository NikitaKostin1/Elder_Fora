from ai import connection as AI
from create_bot import dp, bot
from aiogram import types
from config import logger
from misc import util


@logger.catch
async def start_bot(message: types.Message):
	"""
	/start command
	"""
	CUSTOMER_ID = message["from"]["id"]
	await message.answer(message)
	await message.answer("👋")




@logger.catch
async def general(message: types.Message):
	CUSTOMER_ID = message["from"]["id"]
	prompt = message["text"]
	
	response = await AI.get_response(prompt)
	await util.send_long_message(CUSTOMER_ID, response)
