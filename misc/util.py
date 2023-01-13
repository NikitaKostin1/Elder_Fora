from config import logger
from create_bot import bot


@logger.catch
async def send_long_message(CUSTOMER_ID: int, text: str) -> list:
	"""
	Splits texts into max allowed length for telegram message
	And sends it
	"""
	messages = list()

	if not text:
		logger.error(f"{CUSTOMER_ID}: {text=}")
		return messages

	if len(text) > 4096:

		for x in range(0, len(text), 4096):
			try:
				msg = await bot.send_message(CUSTOMER_ID, text[x:x+4096])
			except:
				msg = await bot.send_message(CUSTOMER_ID, text[x:x+4096].replace("<", "").replace(">", ""))

			messages.append(msg)

	else:
		msg = await bot.send_message(CUSTOMER_ID, text)
		messages.append(msg)

	return messages
