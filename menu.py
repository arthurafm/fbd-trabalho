import queries
from pick import pick
import os

def openMenu():
    conn = queries.openDatabase()
    title = 'Por favor selecione uma operação:'
    while True:
        options = [
            'Consulta para achar as matérias lidas por usuários',
            'Consulta para achar o nome dos usuários e os animes colocados como Assistir Depois',
            'Consulta para achar o nome e id dos usuarios que tem que pagar a sua fatura no dia 30/03/2022',
            'Ordena animes a partir de certo ano e a partir de uma certa nota',
            'Consulta um anime a partir de certa quantidade de "gostei" em seus episódios',
            'Consulta para achar animes de certo genero com mais de certa quantidade de episodios',
            'Consulta para achar os usuários que assistiram o vídeo de maior duração',
            'Consulta todos os animes de mesma lista de Assistir Depois do usuário de id 325265 e mesmo gênero de Chainsaw Man de id 53153',
            'Consulta para buscar histórico do usuário  durante a temporada Outono/22',
            'Consulta para buscar os Shounens de Outono/22 dentro de uma determinada Crunchylista',
            'Consulta de visualizações',
            'Inserir visualização',
            'Sair'
        ]
        option, index = pick(options, title)
        if index == 12:
            break
        elif index == 11:
            queries.insertVisualization(conn)
        else:
            if index in range(3, 6):
                sub_title = 'Deseja alterar os parâmetros?'
                sub_options = ['Sim', 'Não']
                sub_option, sub_index = pick(sub_options, sub_title)
                if sub_index == 0:
                    queries.changeParameters(index)
            print('\n' + option + ':')
            queries.select(conn, index)
        print('\nDigite qualquer coisa para continuar...', end='')
        input()
        os.system('cls')
    queries.closeDatabase(conn)
