from PIL import ImageTk
import PySimpleGUI as sg
from config import Config
from prompt import Prompt
from chat_assistant import ChatAssistant
from image_fetcher import ImageFetcher

class App:
    def __init__(self):
        self.config = Config()
        self.config.validate()
        self.prompt = Prompt()
        self.chat_assistant = ChatAssistant(self.config.openai_api_key)
        self.image_fetcher = ImageFetcher()

    @staticmethod
    def update_window_with_image(window, key, image):
        image.thumbnail((333, 333))
        window[key].update(data=ImageTk.PhotoImage(image))

    def conversar_com_personagem(self, nome, idade, moradia, humor, personagem, mensagem):
        mensagem = self.prompt.gera_prompt(nome, idade, moradia, humor, personagem)
        self.chat_assistant.adicionar_mensagem("system", mensagem)
        self.chat_assistant.adicionar_mensagem("user", mensagem)
        resposta = ""
        while not resposta.endswith('.'):
            resposta = self.chat_assistant.enviar_solicitacao()
            self.chat_assistant.adicionar_mensagem("assistant", resposta)
            self.chat_assistant.remover_excesso_tokens()
            if resposta and resposta[0] == ' ': resposta = resposta[1:]
            if resposta and resposta[-1] == ' ': resposta = resposta[:-1]
        return resposta.strip()

    def main(self):
        layout = [
            [sg.Text("Qual o seu nome? "), sg.Input(key='-NOME-', size=(30,), enable_events=False)],
            [sg.Text("Qual a sua idade? "), sg.Input(key='-IDADE-', size=(30,), enable_events=False)],
            [sg.Text("Onde você mora? "), sg.Input(key='-MORADIA-', size=(30,), enable_events=False)],
            [sg.Text("Como você está se sentindo agora? "), sg.Input(key='-HUMOR-', size=(30,), enable_events=False)],
            [sg.Text("Com quem você quer falar? "), sg.Input(key='-PERSONAGEM-', size=(30,), enable_events=True)],
            [sg.Text("Escreva a mensagem, diga ou pergunte algo: "), sg.Input(key='-MENSAGEM-', size=(75,), enable_events=False)],
            [sg.Button("Enviar mensagem ou pergunta"), sg.Button("Sair")],
            [sg.Image(key='-IMAGE1-', size=(201, 201)), sg.Output(size=(30, 10), key='-OUTPUT1-', expand_x=True, expand_y=True), sg.Image(key='-IMAGE2-', size=(201, 201))],
        ]

        window = sg.Window("Simulador de Personagens - by René - Versão ALPHA 3", layout, resizable=True)

        while True:
            try:
                event, values = window.read(timeout=100)

                if event in (sg.WIN_CLOSED, "Sair"):
                    break

                if event == '-PERSONAGEM-':
                    window['-OUTPUT1-'].update('')
                    window['-IMAGE1-'].update(data=None)
                    window['-IMAGE2-'].update(data=None)
                    self.chat_assistant.historico_mensagens.clear()

                elif event == "Enviar mensagem ou pergunta":
                    values = window.read()[1]  # Obtém os valores do formulário
                    nome = values['-NOME-']
                    idade = int(values['-IDADE-'])  # Converte a idade para inteiro
                    if idade <= 17:
                        filtro_familia = "Strict"
                    elif 18 <= idade <= 59:
                        filtro_familia = "Off"
                    else:
                        filtro_familia = "Moderate"
                    moradia = values['-MORADIA-']
                    humor = values['-HUMOR-']
                    personagem = values['-PERSONAGEM-']
                    mensagem = values['-MENSAGEM-']
                    self.mensagem = self.prompt.gera_prompt(nome, idade, moradia, humor, personagem)
                    resposta = self.conversar_com_personagem(nome, idade, moradia, humor, personagem, mensagem)
                    window['-OUTPUT1-'].print(f"{personagem.upper()} DIZ:\n{resposta}\n\n")
                    
                    images = self.image_fetcher.download_personagem_image(personagem, filtro_familia)
                    for i, image in enumerate(images[:2]):
                        self.update_window_with_image(window, f'-IMAGE{i+1}-', image)
            
            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")
    
        window.close()

app = App()
app.main()