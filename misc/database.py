from psycopg2 import extensions
from datetime import datetime
from config import logger



@logger.catch
def user_exists(cursor: extensions.cursor, USER_ID: int) -> bool:
	"""
	Checks if user exists in db by chat_id
	Returns True if exist
	"""
	cursor.execute(f"SELECT * FROM users WHERE id = {USER_ID};")
	is_user = cursor.fetchone()

	return bool(is_user)



@logger.catch
def add_user(connection: extensions.connection, cursor: extensions.cursor, user_data: dict) -> bool:
	"""
	INSERT INTO users table new user by user_data dict variable (all params are neccesery)
	Returns True in case of successful operation
	"""
	try:
		cursor.execute(f"""
			INSERT INTO users VALUES(
				{user_data['user_id']},
				'{user_data['username']}',
				'{user_data['visit_date']}',
				'{user_data['visit_time']}'
			);
		""")
		connection.commit()

		return True
	except Exception as e:
		logger.error(e)
		logger.error(user_data)
		return False
