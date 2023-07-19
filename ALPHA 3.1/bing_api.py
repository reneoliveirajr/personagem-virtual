from io import BytesIO
import requests

from PIL import Image
import PySimpleGUI as sg

from config import Config


class BingAPI:
    def __init__(self):
        config = Config()
        self.subscription_key = config.bing_api_key
        self.filtro_familia = {(0, 17): "Strict", (18, 59): "Off", (60, float("inf")): "Moderate"}

    def obter_imagem(self, idade, personagem):
        search_url = "https://api.bing.microsoft.com/v7.0/images/search"
        headers = {"Ocp-Apim-Subscription-Key": self.subscription_key}
        safesearch = next((valor for faixa, valor in self.filtro_familia.items() if faixa[0] <= idade <= faixa[1]), None)
        params = {"q": personagem, "count": 10, "safesearch": safesearch, "maxFileSize": 170666}
        
        with requests.Session() as sessao_tcp:
            response = sessao_tcp.get(search_url, headers=headers, params=params)
            try:
                response.raise_for_status()
            except(requests.exceptions.RequestException) as erro:
                sg.popup (
                    f"Erro na requisição para a API do Bing!\n\n"
                    f"Erro: {erro}\n\nNão será possível baixar imagens dessa vez.",
                    title="Falha na Chamada para a API do Bing"
                )
                return
            search_result = response.json()
            imagens_obtidas = []
            for resultado in search_result["value"]:
                response = sessao_tcp.get(resultado["thumbnailUrl"], stream=True)
                try:
                    response.raise_for_status()
                except(requests.exceptions.RequestException) as erro:
                    sg.popup(
                        f"Erro na requisição de uma imagem!\n\n\n"
                        f"Erro: {erro}",
                        title="Falha no Download de Imagem"
                    )
                dados_da_imagem = BytesIO()
                for chunk in response.iter_content(chunk_size=8192):
                    dados_da_imagem.write(chunk)
                dados_da_imagem.seek(0)
                try:
                    imagem = Image.open(dados_da_imagem)
                except IOError as erro:
                    sg.popup(f"Erro ao lidar com imagem!\n\n\nErro: {erro}",
                             title="Erro com a imagem"
                    )
                    continue
                imagens_obtidas.append(imagem)
        return imagens_obtidas