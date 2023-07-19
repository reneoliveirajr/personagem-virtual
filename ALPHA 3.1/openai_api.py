import PySimpleGUI as sg
import openai

from config import Config


class OpenAIBOT:
    def __init__(self, nome, idade, moradia, humor, personagem, mensagem):
        self.nome = nome
        self.idade = idade
        self.moradia = moradia
        self.humor = humor
        self.personagem = personagem
        self.mensagem = mensagem
        config = Config()
        self.openai_api_key = config.openai_api_key
        openai.api_key = self.openai_api_key

    def gerar_prompt(self, historico):
        self.TRECHO_FINAL_PROMPT = (
            f"Qual seria a sua resposta ou ação, como o(a) {self.personagem} "
            f"responderia em primeira pessoa?"
        )
        anamnase = (
            f"ChatGPT, suponha que você seja o(a) {self.personagem}. Você "
            f"deve responder, conversar ou interagir como ele(a) faria, "
            f"usando o jeito de falar ou agir dele(a) ({self.personagem})."
            f"Considere que quem lhe emite a mensagem, pergunta ou age é "
            f"alguém chamado(a) {self.nome}, que tem {self.idade} anos de "
            f"idade, responda de forma adequada para a idade dele(a). "
            f"{self.nome} mora em {self.moradia} e está se sentindo "
            f"{self.humor}."
        )
        prompt = f"{anamnase} {historico} {self.mensagem} {self.TRECHO_FINAL_PROMPT}"
        return prompt

    def enviar_prompt(self, historico):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=self.gerar_prompt(historico),
                temperature=0.3,  # grau de aleatoriedade das respostas
                max_tokens=216,  # tamanho da resposta
                top_p=0.6,  # parâmetro de amostragem núcleo
                frequency_penalty=0.3,  # penalidade por frequência
                presence_penalty=0.9,  # penalidade por presença
            )
            resposta = response.choices[0].text.strip()
            return resposta
        except openai.OpenAIError as erro:
            sg.popup(f"Erro ao conversar com o personagem!\n\n\nErro: {erro}", title="OpenAIError")