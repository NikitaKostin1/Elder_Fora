# from keyboards import inline_ru, inline_en, reply_ru, reply_en
# from assets import texts_ru, texts_en
from loguru import logger
# import psycopg2
import openai
import os

TOKEN = os.getenv("BOT_TOKEN") # bot token
openai.api_key = os.getenv("AI_TOKEN") # opanai token
openai.api_url = "https://api.openai.com"

logger.add(
	"debug.log",		# logs writes into debug.log file
	format="{level} {message}",
	level="WARNING",	# warning logs and its parents writes only
	rotation="1 MB",	# if file exceed 1MB size new file creates
	compression="zip"	# old logs files has .zip compression
)

# def get_conn():
# 	"""
# 	returns psycopg2.extensions.connection object from Heroku server
# 	"""
# 	DATABASE_URL = os.getenv("DATABASE_URL")
# 	connection = psycopg2.connect(DATABASE_URL, sslmode="require")

# 	return connection

