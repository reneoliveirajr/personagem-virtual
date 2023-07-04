import configparser
from dotenv import load_dotenv
import PySimpleGUI as sg
import sys
import os

class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.env')
        if getattr(sys, 'frozen', False):
            self.bing_api_key = config.get('Keys', 'BING_API_KEY')
            self.openai_api_key = config.get('Keys', 'OPENAI_API_KEY')
        else:
            load_dotenv('config.env')
            self.bing_api_key = os.getenv('BING_API_KEY')
            self.openai_api_key = os.getenv('OPENAI_API_KEY')

    def validate(self):
        if not self.bing_api_key and not self.openai_api_key:
            sg.popup('Erro: As chaves do Bing API e do ChatGPT não estão especificadas.\nConfigure suas chaves no arquivo config.env no mesmo diretório do programa.', title="Faltam as chaves... ;)")
            sys.exit(1)
        elif not self.bing_api_key:
            sg.popup('Erro: A chave do Bing API não está especificada.', title="Bing API")
            sys.exit(1)
        elif not self.openai_api_key:
            sg.popup('Erro: A chave do ChatGPT não está especificada.', title="ChatGPT API")
            sys.exit(1)