from create_bot import bot
from aiogram import types
from config import logger
from typing import Dict


class MessageHandler:
	def __init__(self):
		self.storage: Dict[int, types.Message] = {}


	@logger.catch
	async def acquire(self, message: types.Message) -> None:
		USER_ID = message["chat"]["id"]

		if USER_ID in self.storage:
			await self.edit(USER_ID)

		self.storage[USER_ID] = message


	@logger.catch
	async def release(self, USER_ID: int) -> types.Message:
		if not USER_ID in self.storage:
			return

		message = self.storage[USER_ID]
		self.storage[USER_ID] = None

		return message



	@logger.catch
	async def edit(self, USER_ID: int, text: str=None, markup: types.InlineKeyboardMarkup=None) -> None:
		if not USER_ID in self.storage:
			return
		
		message = self.storage[USER_ID]
		message_id = message["message_id"]

		if not text:
			if "text" in message:
				text = message["text"]
			else:
				text = message["caption"]

		try:
			await bot.edit_message_text(
				chat_id=USER_ID,
				message_id=message_id,
				text=text,
				reply_markup=markup,
				disable_web_page_preview=True
			)
		except:
			pass


	@logger.catch
	async def delete(self, USER_ID: int) -> None:
		if not USER_ID in self.storage:
			return

		message = await self.release(USER_ID)

		try:
			await message.delete()
		except:
			pass
			



MainMessage = MessageHandler()