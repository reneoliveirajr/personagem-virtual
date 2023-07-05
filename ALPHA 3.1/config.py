import os
import re
import sys
import configparser
from dotenv import load_dotenv
import PySimpleGUI as sg
from encerra import Encerra

PADRAO_OPENAI = r"^sk-[A-Za-z0-9]{48}$"
PADRAO_BING = r"^[0-9a-f]{32}$"

class Config:
    def __init__(self):
        if getattr(sys, "frozen", False):
            config = configparser.ConfigParser()
            config.read("config.env")
            self.bing_api_key = config.get("Keys", "BING_API_KEY")
            self.openai_api_key = config.get("Keys", "OPENAI_API_KEY")
        else:
            load_dotenv("config.env")
            self.bing_api_key = os.getenv("BING_API_KEY")
            self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def exibe_erro_e_fecha(self, mensagem, titulo):
        sg.popup(mensagem, title=titulo)
        Encerra.encerra()

    def validar_existencia_chaves(self):
        if not self.openai_api_key and not self.bing_api_key:
            self.exibe_erro_e_fecha("Erro: As chaves da OpenAI e do Bing não estão especificadas.\nConfigure suas chaves no arquivo config.env no mesmo diretório do programa.", "Chaves Não Encontradas")
        elif not self.openai_api_key:
            self.exibe_erro_e_fecha("Erro: A chave da OpenAI não está especificada.", "OpenAI Key API Not Found")
        elif not self.bing_api_key:
            self.exibe_erro_e_fecha("Erro: A chave do Bing API não está especificada.", "Bing API Key Not Found")

    def verificar_chave_openai(self):
        return not re.match(PADRAO_OPENAI, self.openai_api_key)

    def verificar_chave_bing(self):
        return not re.match(PADRAO_BING, self.bing_api_key)

    def chaves_incorretas(self):
        if self.verificar_chave_openai() and self.verificar_chave_bing():
            self.exibe_erro_e_fecha("Erro: Ambas as chaves do Bing API e da OpenAI estão incorretas.\nVerifique o formato das chaves e tente novamente.", "Chaves Incorretas")
        elif self.verificar_chave_openai():
            self.exibe_erro_e_fecha("Erro: A chave da OpenAI está incorreta.", "OpenAI API Key Format Error")
        elif self.verificar_chave_bing():
            self.exibe_erro_e_fecha("Erro: A chave do Bing está incorreta.", "Bing API Key Format Error")