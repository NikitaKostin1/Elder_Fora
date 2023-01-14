from config import logger, openai
from aiohttp import ClientSession
import json


class Response:
	def __init__(self, model: str, prompt: str):
		self.model = model
		self.prompt = prompt


	@logger.catch
	async def get(self) -> str:
		"""
		Returns str answer or image URL
		"""
		options = {
			"text-davinci-003": self.chat,
			"image-alpha-001": self.image
		}
		return await options[self.model]()


	@logger.catch
	async def chat(self) -> str:
		"""
		Returns str as chat answer
		"""
		async with ClientSession() as session:
			headers = {
				"Content-Type": "application/json",
				"Authorization": f"Bearer {openai.api_key}"
			}
			data = {
				"prompt": self.prompt,
				"temperature": 0.5,
				"max_tokens": 1800,
				"top_p": 1.0,
				"frequency_penalty": 0.5,
				"presence_penalty": 0.0
			}
			url = f"{openai.api_url}/v1/engines/{self.model}/completions"

			async with session.post(url, json=data, headers=headers) as resp:
				json_response = await resp.json()
				return json_response['choices'][0]['text']


	@logger.catch
	async def image(self) -> str:
		"""
		Returns image URL
		"""
		response = openai.Image.create(prompt=self.prompt, model=self.model)

		return response["data"][0]["url"]
