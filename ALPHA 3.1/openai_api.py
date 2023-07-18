import openai
import PySimpleGUI as sg
from config import Config

class OpenAI:
    def __init__(self, nome, idade, moradia, humor, personagem, mensagem):
        self.nome = nome
        self.idade = idade
        self.moradia = moradia
        self.humor = humor
        self.personagem = personagem
        self.mensagem = mensagem
        self.TRECHO_FINAL_PROMPT = (
            f"Qual seria a sua resposta, ou ação; como o(a) {personagem} "
            f"responderia em primeira pessoa?"
        )
        config = Config()
        self.openai_api_key = config.openai_api_key
        openai.api_key = self.openai_api_key
        
    def gera_anamnase(self):
        anamnase = (
            f"ChatGPT, suponha que você é {self.personagem}. Você deve responder, "
            f" conversar ou interagir como esse personagem faria, utilizando "
            f"jeito de falar ou agir desse personagem ({self.personagem}). "
            f"Considere que quem lhe emite a mensagem, pergunta ou age é "
            f"alguém chamado(a) {self.nome}, que tem {self.idade} anos de idade, "
            f"trate-o(a) como tal, ou seja, respondendo de forma adequada "
            f"para sua idade, mora em {self.moradia} e está se sentindo {self.humor}."
        )
        return anamnase

    def gera_prompt(self):
        prompt = f"{self.gera_anamnase()} {self.mensagem} {self.TRECHO_FINAL_PROMPT}"
        return prompt

    def enviar_prompt(self):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=self.gera_prompt(),
                temperature=0.2,
                max_tokens=300,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=1,
            )
            resposta = response.choices[0].text.strip()
            return resposta
        except openai.OpenAIError as erro:
            sg.popup(f"Erro ao conversar com o personagem!\n\n\nErro: {erro}", title="OpenAIError")
