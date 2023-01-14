from create_bot import dp, Dispatcher
from . import client, callbacks


def register_general_handlers(dp: Dispatcher):
	"""
	Registers all general (visible) commands
	"""
	# COMMANDS
	dp.register_message_handler(client.start_bot, commands=["start"], state="*")

	# REPLY MARKUP 
	dp.register_message_handler(client.ai_model_choice, lambda message: message.text == "Режим ⚙️")

	# CALLBACKS
	dp.register_callback_query_handler(callbacks.set_ai_model, lambda query: query.data.split()[0] == "ai_model")

	# PROMPT INPUT
	dp.register_message_handler(client.general, lambda message: message.text)