from create_bot import dp, Dispatcher
from . import client


def register_general_handlers(dp: Dispatcher):
	"""
	Registers all general (visible) commands
	"""
	# COMMANDS
	dp.register_message_handler(client.start_bot, commands=["start"], state="*")

	# TEXT INPUT
	dp.register_message_handler(client.general, lambda message: message.text)	
