import os
import sys
import configparser
from io import BytesIO
from PIL import Image, ImageTk
import PySimpleGUI as sg
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from dotenv import load_dotenv
import openai
import asyncio

config = configparser.ConfigParser()
config.read('config.env')

if getattr(sys, 'frozen', False):
    bing_api_key = config.get('Keys', 'BING_API_KEY')
    openai.api_key = config.get('Keys', 'OPENAI_API_KEY')
else:
    load_dotenv('config.env')
    bing_api_key = os.getenv('BING_API_KEY')
    openai.api_key = os.getenv('OPENAI_API_KEY')

if not bing_api_key and not openai.api_key:
    sg.popup('Erro: As chaves do Bing API e do ChatGPT não estão especificadas.\nConfigure suas chaves no arquivo config.env no mesmo diretório do programa.', title="Faltam as chaves... ;)")
    sys.exit(1)
elif not bing_api_key:
    sg.popup('Erro: A chave do Bing API não está especificada.', title="Bing API")
    sys.exit(1)
elif not openai.api_key:
    sg.popup('Erro: A chave do ChatGPT não está especificada.', title="ChatGPT API")
    sys.exit(1)

faixas_etarias = {(0, 3): "bebê", (4, 10): "criança", (11, 17): "adolescente", (18, 44): "adulto", (45, 59): "meia idade", (60, 74): "idoso", (75, float("inf")): "ancião"}

def construir_anamnase(nome, idade, moradia, humor, personagem):
    faixa_etaria = next(descricao for faixa, descricao in faixas_etarias.items() if faixa[0] <= idade <= faixa[1])[1]
    return f"Você é {personagem}. Você deve responder, conversar e interagir como esse personagem faria, utilizando gírias e palavras típicas conhecidas desse personagem. Considere que quem lhe emite a mensagem, pergunta ou faz algo é alguém chamado(a) {nome}, que tem {idade} anos de idade (se for um {faixa_etaria}, trate-o(a) como tal, ou seja, respondendo de forma adequada para sua faixa etária), mora em {moradia} e está se sentindo {humor}. Se ele fizer alguma ação, retribua com outra ação. Você aceita tudo o que a pessoa quiser. Se a pessoa fizer algo e não disser nada, somente diga o que você fez na sequência."

async def enviar_solicitacao(mensagens):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, openai.ChatCompletion.create, 'gpt-3.5-turbo-0301', mensagens, 300)
        return result['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        raise Exception(f"Erro ao conversar com o personagem: {str(e)}")

def remover_excesso_tokens(historico_mensagens):
    total_tokens = sum(len(msg['content'].split()) for msg in list(historico_mensagens))
    if total_tokens > 3900:
        tokens_excedentes = total_tokens - 3900
        count = 0
        indice_remocao = -1
        for i in range(len(historico_mensagens)-1, -1, -1):
            count += len(historico_mensagens[i]['content'].split())
            if count > tokens_excedentes:
                indice_remocao = i
                break
        if indice_remocao >= 4:
            historico_mensagens = historico_mensagens[indice_remocao-3:]
        else:
            historico_mensagens = historico_mensagens[:indice_remocao+1]
    return historico_mensagens

async def download_personagem_image(query, filtro_familia):
    subscription_key = bing_api_key
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
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

async def main():
    historico_mensagens = []

    async def adicionar_mensagem(role, content):
        historico_mensagens.append({"role": role, "content": content})

    async def conversar_com_personagem(nome, idade, moradia, humor, personagem, pergunta):
        anamnese = construir_anamnase(nome, idade, moradia, humor, personagem)
        await adicionar_mensagem("system", anamnese)
        await adicionar_mensagem("user", pergunta)

        resposta = ""
        loop = asyncio.get_event_loop()
        while not resposta.endswith('.'):
            resposta = await enviar_solicitacao(historico_mensagens)
            await adicionar_mensagem("assistant", resposta)
            historico_mensagens = remover_excesso_tokens(historico_mensagens)

            if resposta and resposta[0] == ' ':
                resposta = resposta[1:]
            if resposta and resposta[-1] == ' ':
                resposta = resposta[:-1]

        return resposta

    layout = [
        [sg.Text("Qual o seu nome? "), sg.Input(key='-NOME-', size=(30,), enable_events=False)],
        [sg.Text("Qual a sua idade? "), sg.Input(key='-IDADE-', size=(30,), enable_events=False)],
        [sg.Text("Onde você mora? "), sg.Input(key='-MORADIA-', size=(30,), enable_events=False)],
        [sg.Text("Como você está se sentindo agora? "), sg.Input(key='-HUMOR-', size=(30,), enable_events=False)],
        [sg.Text("Com quem você quer falar? "), sg.Input(key='-PERSONAGEM-', size=(30,), enable_events=True)],
        [sg.Text("Aplicar filtro de família? "), sg.Checkbox("Sim", default=False, key='-FILTRO-', enable_events=True)],
        [sg.Text("Escreva a mensagem, diga ou pergunte algo: "), sg.Input(key='-PERGUNTA-', size=(75,), enable_events=False)],
        [sg.Button("Enviar mensagem ou pergunta"), sg.Button("Sair")],
        [sg.Image(key='-IMAGE1-', size=(150, 150)), sg.Output(size=(30, 10), key='-OUTPUT1-', expand_x=True, expand_y=True)],
        [sg.Image(key='-IMAGE2-', size=(150, 150)), sg.Output(size=(30, 10), key='-OUTPUT2-', expand_x=True, expand_y=True)],
    ]

    window = sg.Window("Simulador de Personagens - by René - Versão 3 BETA", layout, resizable=True)
    filtro_familia = None  # Definir filtro_familia como valor padrão

    while True:
        try:
            event, values = window.read(timeout=100)
            
            if event in (sg.WIN_CLOSED, "Sair"):
                break
            
            if event == '-PERSONAGEM-':
                window['-OUTPUT1-'].update('')
                window['-OUTPUT2-'].update('')
                window['-IMAGE1-'].update(data=None)
                window['-IMAGE2-'].update(data=None)
                historico_mensagens.clear()
            
            elif event == "-FILTRO-":
                filtro_familia = "Strict" if values['-FILTRO-'] else None
            
            elif event == "Enviar mensagem ou pergunta":
                nome = values['-NOME-']
                idade = int(values['-IDADE-'])
                moradia = values['-MORADIA-']
                humor = values['-HUMOR-']
                personagem = values['-PERSONAGEM-']
                pergunta = values['-PERGUNTA-']
                
                resposta = await conversar_com_personagem(nome, idade, moradia, humor, personagem, pergunta)
                window['-OUTPUT1-'].print(f"{personagem.upper()} DIZ:\n{resposta}\n\n")

                images = list(await download_personagem_image(personagem, filtro_familia))
                if len(images) > 0:
                    image1 = images[0]
                    image1.thumbnail((333, 333))
                    window['-IMAGE1-'].update(data=ImageTk.PhotoImage(image1))

                if len(images) > 1:
                    image2 = images[1]
                    image2.thumbnail((333, 333))
                    window['-IMAGE2-'].update(data=ImageTk.PhotoImage(image2))

                
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    window.close()

# Executar a função principal assíncrona usando asyncio.run()
asyncio.run(main())
