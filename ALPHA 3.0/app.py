import os
import shutil
import sys
from PIL import ImageTk
import PySimpleGUI as sg
from chat_assistant import ChatAssistant
from config import Config
from image_fetcher import ImageFetcher
from prompt import Prompt
import concurrent.futures

class App:
    def __init__(self):
        self.config = Config()
        self.config.validate()
        self.prompt = Prompt()
        self.chat_assistant = ChatAssistant(self.config.openai_api_key)
        self.image_fetcher = ImageFetcher()

        self.filtro_familia_map = {
            (0, 17): "Strict",
            (18, 59): "Off",
            (60, float("inf")): "Moderate"
        }

    @staticmethod
    def update_window_with_image(window, key, image):
        image.thumbnail((333, 333))
        window[key].update(data=ImageTk.PhotoImage(image))

    def conversar_com_personagem(self, nome, idade, moradia, humor, personagem, mensagem):
        mensagem_gerada = self.prompt.gera_prompt(nome, idade, moradia, humor, personagem, mensagem)
        self.chat_assistant.adicionar_mensagem("system", mensagem_gerada)
        self.chat_assistant.adicionar_mensagem("user", mensagem_gerada)
        resposta = ""
        while not resposta.endswith('.'):
            resposta = self.chat_assistant.enviar_solicitacao()
            self.chat_assistant.adicionar_mensagem("assistant", resposta)
            self.chat_assistant.remover_excesso_tokens()
            if resposta and resposta[0] == ' ': resposta = resposta[1:]
            if resposta and resposta[-1] == ' ': resposta = resposta[:-1]
        return resposta.strip()

    def download_images(self, personagem, filtro_familia):
        return self.image_fetcher.download_personagem_image(personagem, filtro_familia)

    def main(self):
        layout = [
            [sg.Text("Qual o seu nome? "), sg.Input(key='-NOME-', size=(30,), enable_events=False)],
            [sg.Text("Qual a sua idade? "), sg.Input(key='-IDADE-', size=(30,), enable_events=False)],
            [sg.Text("Onde você mora? "), sg.Input(key='-MORADIA-', size=(30,), enable_events=False)],
            [sg.Text("Como você está se sentindo agora? "), sg.Input(key='-HUMOR-', size=(30,), enable_events=False)],
            [sg.Text("Com quem você quer falar? "), sg.Input(key='-PERSONAGEM-', size=(30,), enable_events=True)],
            [sg.Text("Escreva a mensagem, diga ou pergunte algo: "), sg.Input(key='-MENSAGEM-', size=(100,), enable_events=False)],
            [sg.Button("Enviar mensagem ou pergunta"), sg.Button("Sair")],
            [sg.Image(key='-IMAGE1-', size=(400, 300)), sg.Output(size=(40, 20), key='-OUTPUT1-', expand_x=True, expand_y=True), sg.Image(key='-IMAGE2-', size=(400, 300))],
        ]

        window = sg.Window("Simulador de Personagens - by René - Versão ALPHA 3.0", layout, resizable=True)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                try:
                    event, values = window.read(timeout=100)

                    if event == sg.WIN_CLOSED or event == "Sair":
                        # Obtenha o caminho completo para a pasta _pycache_
                        cache_dir = os.path.join(os.getcwd(), '__pycache__')

                        # Verifique se a pasta existe
                        if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
                            # Remova a pasta e seu conteúdo
                            shutil.rmtree(cache_dir)
                        sys.exit()

                    if event == '-PERSONAGEM-':
                        window['-OUTPUT1-'].update('')
                        window['-IMAGE1-'].update(data=None)
                        window['-IMAGE2-'].update(data=None)
                        self.chat_assistant.historico_mensagens.clear()

                    elif event == "Enviar mensagem ou pergunta":
                        nome = values['-NOME-']
                        idade = int(values['-IDADE-'])  # Converte a idade para inteiro
                        filtro_familia = next((valor for faixa, valor in self.filtro_familia_map.items() if faixa[0] <= idade <= faixa[1]), None)
                        moradia = values['-MORADIA-']
                        humor = values['-HUMOR-']
                        personagem = values['-PERSONAGEM-']
                        mensagem = values['-MENSAGEM-']

                        self.mensagem = self.prompt.gera_prompt(nome, idade, moradia, humor, personagem, mensagem)
                        resposta = self.conversar_com_personagem(nome, idade, moradia, humor, personagem, mensagem)
                        window['-OUTPUT1-'].print(f"{personagem.upper()} DIZ:\n{resposta}\n\n")

                        future = executor.submit(self.download_images, personagem, filtro_familia)
                        images = future.result()
                        for i, image in enumerate(images[:2]):
                            if isinstance(image, str):
                                window['-OUTPUT1-'].print(image)
                            else:
                                self.update_window_with_image(window, f'-IMAGE{i+1}-', image)

                except Exception as e:
                    error_message = f"Ocorreu um erro inesperado: {e}"
                    print(error_message)
                    window['-OUTPUT1-'].print(error_message)