# from handlers.admin import main as admin_registrator
from handlers import main as general_registrator
# from checkers import deposit_generator, mailing, todays_users#, dynamic_income
from aiogram import executor
from create_bot import dp
from config import logger
# import tools


async def on_startup(_):
	logger.success("The bot is online!")


# admin_registrator.register_admin_handlers(dp)
general_registrator.register_general_handlers(dp)

# Long-polling launch
if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

