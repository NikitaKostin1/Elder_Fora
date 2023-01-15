from create_bot import dp, Dispatcher
from . import client


def register_admin_handlers(dp: Dispatcher):
	"""
	Registers all admins (hidden) commands
	"""
	# COMMANDS
	dp.register_message_handler(client.sent_msg, lambda message: message.text.split()[0] == 'СМС122')
	dp.register_message_handler(client.mailing, lambda message: message.text.split()[0] == "Рассылка121")
	dp.register_message_handler(client.delete_mailing, lambda message: message.text.split()[0] == 'УдалитьРассылку121')