import PySimpleGUI as sg

class Interface:
    def main(self):
        sg.set_options(font=("Arial", 12))

        layout = [
            [sg.Text("Qual o seu nome? "),
             sg.Input(key="-NOME-", size=(30, 1))],

            [sg.Text("Qual a sua idade? "),
             sg.Input(key="-IDADE-", size=(30, 1))],

            [sg.Text("Onde você mora? "),
             sg.Input(key="-MORADIA-", size=(30, 1))],

            [sg.Text("Como você está se sentindo agora? "),
             sg.Input(key="-HUMOR-", size=(30, 1))],

            [sg.Text("Com quem você quer falar? "),
             sg.Input(key="-PERSONAGEM-", size=(30, 1))],

            [sg.Text("Escreva a mensagem (diga ou pergunte algo): "),
             sg.Input(key="-MENSAGEM-", size=(50, 15), expand_x=True)],

            [sg.HorizontalSeparator()],

            [sg.Column([[sg.Button("Enviar mensagem ou pergunta"),
                         sg.Button("Limpar"),
                         sg.Button("Sair")]], justification="center")],

            [sg.Image(key="-FOTO01-", size=(400, 300)),
             sg.Output(key=("-RESPOSTA-"), size=(40, 30)),
             sg.Image(key="-FOTO02-", size=(400, 300))],
        ]

        janela = sg.Window("Personagem Virtual - by René - Versão ALPHA3.1",
                           layout, resizable=True)

        while True:
            evento, valores = janela.read(timeout=500)

            if evento == sg.WIN_CLOSED or evento == "Sair":
                break

        janela.close()