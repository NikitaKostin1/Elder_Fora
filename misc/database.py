from psycopg2 import extensions
from datetime import datetime
from config import logger



@logger.catch
def user_exists(cursor: extensions.cursor, USER_ID: int) -> bool:
	"""
	Checks if user exists in db by user_id
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
				'{user_data['visit_time']}',
				'{user_data['ai_model']}'
			);
		""")
		connection.commit()

		return True
	except Exception as e:
		logger.error(e)
		logger.error(user_data)
		return False


@logger.catch
def set_ai_model(connection: extensions.connection, cursor: extensions.cursor, USER_ID: int, model: str) -> bool:
	"""
	Updates ai_model column by user_id in users table
	"""
	try:
		cursor.execute(f"""
			UPDATE users SET ai_model = '{model}' WHERE id = {USER_ID};
		""")
		connection.commit()

		return True
	except Exception as e:
		logger.error(f"{USER_ID}: {e=}")
		return False


@logger.catch
def get_ai_model(cursor: extensions.cursor, USER_ID: int) -> str:
	"""
	Returns ai_model by user_id in users table
	In error case returns empty str
	"""
	try:
		cursor.execute(f"SELECT ai_model FROM users WHERE id = {USER_ID};")
		model = cursor.fetchone()[0]

		return model
	except Exception as e:
		logger.error(f"{USER_ID}: {e=}")
		return ""



@logger.catch
def get_all_users(cursor: extensions.cursor) -> list:
	"""
	Returns all rows from users
	In error case returns empty list
	"""
	try:
		cursor.execute("SELECT * FROM users;")
		users = cursor.fetchall()

		return users
	except:
		return list()
