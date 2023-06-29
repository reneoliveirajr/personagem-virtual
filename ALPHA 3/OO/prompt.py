class Prompt:
    """
    Classe responsável por gerar um prompt para interação com um personagem.
    
    Esta classe contém um dicionário com faixas etárias e seus respectivos rótulos e 
    um método para gerar um prompt de interação baseado em um conjunto de parâmetros.

    O prompt é gerado de forma a declarar quem é o interlocutor (usuário) e o personagem,
    estabelecer como deverá ser a interação entre eles de acordo com as características de ambos.

    Atributos
    ---------
    faixas_etarias: dict
        um dicionário que mapeia faixas etárias para seus rótulos correspondentes.
    
    Métodos
    -------
    gera_prompt(nome: str, idade: int, moradia: str, humor: str, personagem: str) -> str:
        Retorna um prompt de interação para o personagem fornecido.
    """
    
    # Com o método __init__ é inicializado o atributo de caracterização de faixa etária quando a classe Prompt for instanciada.
    def __init__(self):
        self.faixas_etarias = {
            (0, 3): "bebê",
            (4, 10): "criança",
            (11, 17): "adolescente",
            (18, 44): "adulto",
            (45, 59): "meia idade",
            (60, 74): "idosa",
            # float("inf") representa o conceito de infinito para considerarmos qualquer valor de idade depois de 75.
            (75, float("inf")): "anciã"
        }

    def gera_prompt(self, nome, idade, moradia, humor, personagem, mensagem):
        # next itera sobre o gerador na linha seguinte e salva somente a primeira correspondência, evitando um loop sobre todas as possibilidades
        self.faixa_etaria = next(
            # coomprensão de gerador para trazer somente a correspondência que estamos buscando
            descricao for faixa, descricao in self.faixas_etarias.items() if faixa[0] <= idade <= faixa[1]
        )
        
        return (
            f"Vc é {personagem}.Vc responde e interage como {personagem} faria,utilizando gírias ou palavras "
            f"típicas do {personagem}.Considere que quem fala,pergunta ou faz algo é alguém chamado {nome},"
            f"com {idade} anos de idade(sendo {self.faixa_etaria},trate-a como tal,respondendo de forma adequada para sua faixa etária)."
            f"{nome} mora em {moradia} e está se sentindo {humor}."
            f"Se essa pessoa perguntar algo,responda como {personagem} responderia,se fizer alguma ação para vc,{personagem},então "
            f"retribua com outra ação conforme {personagem} faria.Vc aceita tudo o que {nome} quiser."
            f"Se {nome} fizer algo e não disser nada,somente diga o que você fez na sequência.{nome} faz,pergunta ou diz:{mensagem}"
        )