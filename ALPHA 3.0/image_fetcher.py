from PIL import Image
from io import BytesIO
import requests
from config import Config

class ImageFetcher:
    def __init__(self):
        config = Config()
        self.subscription_key = config.bing_api_key

    def download_personagem_image(self, query, filtro_familia):
        search_url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        params = {"q": query, "count": 4, "safesearch": filtro_familia}

        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        images = []
        for result in search_results["value"]:
            try:
                response = requests.get(result["thumbnailUrl"])
                response.raise_for_status()
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                images.append(image)
            except (requests.exceptions.RequestException, IOError) as e:
                erro_obter_imagens = f"Ocorreu um erro inesperado ao obter as imagens: {e}"
                images.append(erro_obter_imagens)
                continue

        return images
