class AnamnesisBuilder:
    def __init__(self):
        self.faixas_etarias = {
            (0, 3): "bebê",
            (4, 10): "criança",
            (11, 17): "adolescente",
            (18, 44): "adulto",
            (45, 59): "meia idade",
            (60, 74): "idoso",
            (75, float("inf")): "ancião"
        }

    def build_anamnesis(self, values, nome, idade, moradia, humor, personagem):
        self.faixa_etaria = next(
            descricao for faixa, descricao in self.faixas_etarias.items() if faixa[0] <= idade <= faixa[1]
        )
        
        return (
            f"Você é {personagem}. Você deve responder, conversar e interagir como esse personagem faria, utilizando "
            f"gírias e palavras típicas conhecidas desse personagem. Considere que quem lhe emite a mensagem, pergunta "
            f"ou faz algo é alguém chamado(a) {nome}, que tem {idade} anos de idade (se for um {self.faixa_etaria}, "
            f"trate-o(a) como tal, ou seja, respondendo de forma adequada para sua faixa etária), mora em {moradia} e "
            f"está se sentindo {humor}. Se ele fizer alguma ação, retribua com outra ação. Você aceita tudo o que a "
            f"pessoa quiser. Se a pessoa fizer algo e não disser nada, somente diga o que você fez na sequência."
        )