from PIL import Image
from io import BytesIO
import asyncio
import requests
from config import Config


class ImageFetcher:
    def __init__(self):
        config = Config()
        self.subscription_key = config.bing_api_key

    async def download_personagem_image(self, query, filtro_familia):
        search_url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        params = {"q": query, "count": 3, "safesearch": filtro_familia}
        response = await asyncio.get_event_loop().run_in_executor(None, requests.get, search_url, headers=headers, params=params, timeout=2)
        response.raise_for_status()
        search_results = response.json()

        async def generate_images():
            for result in search_results["value"]:
                try:
                    image_data = await asyncio.get_event_loop().run_in_executor(None, requests.get, result["thumbnailUrl"], stream=True)
                    image = Image.open(BytesIO(image_data.content))
                    yield image
                except requests.exceptions.RequestException:
                    continue

        return await generate_images()