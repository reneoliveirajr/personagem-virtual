import openai

class ChatAssistant:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key
        self.historico_mensagens = []

    def adicionar_mensagem(self, role, content):
        self.historico_mensagens.append({"role": role, "content": content})

    def enviar_solicitacao(self):
        result = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-0301',
            messages=self.historico_mensagens,
            max_tokens=300
        )
        return result['choices'][0]['message']['content'].strip()

    def remover_excesso_tokens(self):
        total_tokens = sum(len(msg['content'].split()) for msg in self.historico_mensagens)
        if total_tokens > 3900:
            tokens_excedentes = total_tokens - 3900
            count = 0
            indice_remocao = -1
            for i in range(len(self.historico_mensagens)-1, -1, -1):
                count += len(self.historico_mensagens[i]['content'].split())
                if count > tokens_excedentes:
                    indice_remocao = i
                    break
            if indice_remocao >= 4:
                self.historico_mensagens = self.historico_mensagens[indice_remocao-3:]
            else:
                self.historico_mensagens = self.historico_mensagens[:indice_remocao+1]
        return self.historico_mensagens