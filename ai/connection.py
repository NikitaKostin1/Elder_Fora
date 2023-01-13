from config import logger, openai
from aiohttp import ClientSession
import json

@logger.catch
async def get_response(prompt: str) -> str:
	async with ClientSession() as session:
		headers = {
			"Content-Type": "application/json",
			"Authorization": f"Bearer {openai.api_key}"
		}
		data = {
			"prompt": prompt,
			"temperature": 0.5,
			"max_tokens": 2000,
			"top_p": 1.0,
			"frequency_penalty": 0.5,
			"presence_penalty": 0.0
		}
		url = f"{openai.api_url}/v1/engines/text-davinci-003/completions"

		async with session.post(url, json=data, headers=headers) as resp:
			json_response = await resp.json()
			return json_response['choices'][0]['text']
