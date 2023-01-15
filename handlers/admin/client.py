from misc import util, database as db
from config import logger, get_conn
from assets import texts as txt
from create_bot import bot, dp
from aiogram import types


@logger.catch
async def mailing(message: types.Message):
	"""
	Send text to everyone in the bot (from users table)
	"""
	USER_ID = message["from"]["id"]

	try:
		text = "\n".join(message["text"].split("\n")[1:])
		if not text:
			assert False
	except:
		await message.answer(txt.admin_mailing_tip)
		return

	connection = get_conn()
	cursor = connection.cursor()

	users = db.get_all_users(cursor)

	cursor.close()
	connection.close()

	if not users:
		await message.answer(txt.error_message)
		logger.error(f"{USER_ID}: {users=}")
		return

	sent_msgs = []
	blocked_msgs = 0
	blocked_users = []

	for user in users:
		user_id = user[0]
		username = user[1]

		try:
			msg = await bot.send_message(user_id, text, disable_web_page_preview=True)
			sent_msgs.append(msg)
		except Exception as e:
			blocked_msgs += 1
			blocked_users.append(username)

	await message.answer(f"Доставлено: {len(sent_msgs)}. Ошибка: {blocked_msgs}")
	# await util.send_long_message(message["chat"]["id"], "Заблокировали: " + "@"+" @".join(blocked_users))

	mailing.sent_messages = sent_msgs




@logger.catch
async def delete_mailing(message: types.Message):
	try:
		messages = mailing.sent_messages
	except:
		await message.answer("Подождите, пока закончится рассылка или вызовите новую рассылку")
		return

	deleted = 0
	error = 0

	for msg in messages:
		try:
			await msg.delete()
			deleted += 1
		except:
			error += 1

	await message.answer(f"Удалено: {deleted}. Ошибка: {error}")


