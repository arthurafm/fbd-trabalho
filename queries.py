import psycopg2
from prettytable import PrettyTable

class Selection():
    def __init__(self, attributes, junctionTables, conditions, grouping, having, ordering):
        self.attributes = attributes  # SELECT
        self.junctionTables = junctionTables  # FROM
        self.conditions = conditions  # WHERE
        self.grouping = grouping  # GROUP BY
        self.having = having  # HAVING
        self.ordering = ordering  # ORDER BY


def openDatabase():
    try:
        conn = psycopg2.connect(database='Crunchyroll',
                                user='postgres',
                                password='admin',
                                host='127.0.0.1',
                                port='5432')
        return conn
    except:
        print('Erro ao abrir banco de dados.')


def closeDatabase(conn):
    try:
        conn.close()
    except:
        print('Erro ao fechar banco de dados.')


def selectorObj(sel):
    if sel == 0:
        return s0
    elif sel == 1:
        return s1
    elif sel == 2:
        return s2
    elif sel == 3:
        return s3
    elif sel == 4:
        return s4
    elif sel == 5:
        return s5
    elif sel == 6:
        return s6
    elif sel == 7:
        return s7
    elif sel == 8:
        return s8
    elif sel == 9:
        return s9
    elif sel == 10:
        return s10


def createStringSelection(obj):
    returnStr = ''
    returnStr += f'SELECT {obj.attributes}\n'
    returnStr += f'FROM {obj.junctionTables}\n'
    if obj.conditions != '':
        returnStr += f'WHERE {obj.conditions}\n'
    if obj.grouping != '':
        returnStr += f'GROUP BY {obj.grouping}\n'
    if obj.having != '':
        returnStr += f'HAVING {obj.having}\n'
    if obj.ordering != '':
        returnStr += f'ORDER BY {obj.ordering}\n'
    return returnStr


def printSelection(cur, obj):
    rows = cur.fetchall()
    columns = [str(x) for x in (obj.attributes).split(', ') if x.strip()]
    table = PrettyTable()
    table.field_names = columns
    for row in rows:
        table.add_row(row)
    print(table)


def changeParameters(sel):
    if sel == 3:
        s3_ano = int(input("Digite o ano: "))
        s3_nota = float(input("Digite a nota: "))
        global s3
        s3 = Selection('ANIMES.nome, AVG(RESENHAS.nota) AS nota',
                       'RESENHAS NATURAL JOIN ANIMES NATURAL JOIN TEMPORADAS',
                       f'TEMPORADAS.ano > {s3_ano}',
                       'ANIMES.nome',
                       f'AVG(RESENHAS.nota) > {s3_nota}',
                       '')
    elif sel == 4:
        s4_count = int(input("Digite a quantidade de likes: "))
        # Consulta um anime a partir de certa quantidade de "gostei" em seus episódios
        global s4
        s4 = Selection('ANIMES.nome, COUNT(tipo) AS likes',
                       'ANIMES NATURAL JOIN VIDEOS NATURAL JOIN AVALIACOES',
                       '',
                       'ANIMES.nome',
                       f'COUNT(tipo) > {s4_count}',
                       '')

    else:
        s5_genero = input("Digite o genero: ")
        s5_episodios = int(input("Digite o numero de episodios: "))
        global s5_sub1
        s5_sub1 = Selection('anime_id',
                            'VIDEOS',
                            '',
                            'anime_id',
                            f'COUNT(episodio) > {s5_episodios}',
                            '')
        global s5
        s5 = Selection('nome, anime_id',
                       'ANIMES NATURAL JOIN CLASSIFICACOES_GENERO',
                       f"anime_id IN ({createStringSelection(s5_sub1)}) AND nome_genero = '{s5_genero}'",
                       '',
                       '',
                       '')


def select(conn, sel):
    try:
        cur = conn.cursor()
        obj = selectorObj(sel)
        selectionString = createStringSelection(obj)
        cur.execute(selectionString)
        printSelection(cur, obj)
    except:
        print('Erro ao ler tabelas.')


def insertVisualization(conn):
    try:
        cur = conn.cursor()
        user_id = int(input('Digite o user id: '))
        video_id = int(input('Digite o video id: '))
        insertString = 'INSERT INTO VISUALIZACOES\n' \
                       f'VALUES ({user_id}, {video_id}, now())'
        cur.execute(insertString)
        conn.commit()
    except:
        print('Erro ao inserir na tabela.')


# Consulta para achar o nome e titulo de quem leu determinadas materias
s0 = Selection('nome, titulo',
               'NOTICIAS NATURAL JOIN LEITURAS NATURAL JOIN USUARIOS',
               '',
               '',
               '',
               '')
# Consulta para achar o nome do usuário e do anime que ele colocou como Assistir Depois
s1_sub1 = Selection('nome AS nome_usuario, anime_id',
                    'ASSISTIRDEPOIS NATURAL JOIN USUARIOS',
                    '',
                    '',
                    '',
                    '')
s1 = Selection('nome_usuario, nome AS nome_anime',
               f'({createStringSelection(s1_sub1)}) AS foo NATURAL JOIN ANIMES',
               '',
               '',
               '',
               'nome_usuario')

# Consulta para achar o nome e id dos usuarios que tem que pagar a sua fatura em determinado dia
s2_sub1 = Selection('validade, user_id',
                    'FATURA NATURAL JOIN CARTAO',
                    "validade = '2023-03-30'",
                    '',
                    '',
                    '')
s2 = Selection('nome, user_id',
               f'({createStringSelection(s2_sub1)}) AS foo NATURAL JOIN USUARIOS',
               '',
               '',
               '',
               '')

# Ordena animes a partir de certo ano e a partir de uma certa nota
s3_ano = 2000
s3_nota = 4.0
s3 = Selection('ANIMES.nome, AVG(RESENHAS.nota) AS nota',
               'RESENHAS NATURAL JOIN ANIMES NATURAL JOIN TEMPORADAS',
               f'TEMPORADAS.ano > {s3_ano}',
               'ANIMES.nome',
               f'AVG(RESENHAS.nota) > {s3_nota}',
               '')

# Consulta um anime a partir de certa quantidade de "gostei" em seus episódios
s4_count = 1
s4 = Selection('ANIMES.nome, COUNT(tipo) AS likes',
               'ANIMES NATURAL JOIN VIDEOS NATURAL JOIN AVALIACOES',
               '',
               'ANIMES.nome',
               f'COUNT(tipo) > {s4_count}',
               '')

# Consulta para achar animes de certo genero com mais de certa quantidade de episodios
s5_episodios = 1
s5_genero = 'Esportes'
s5_sub1 = Selection('anime_id',
                    'VIDEOS',
                    '',
                    'anime_id',
                    f'COUNT(episodio) > {s5_episodios}',
                    '')

s5 = Selection('nome, anime_id',
               'ANIMES NATURAL JOIN CLASSIFICACOES_GENERO',
               f"anime_id IN ({createStringSelection(s5_sub1)}) AND nome_genero = '{s5_genero}'",
               '',
               '',
               '')

# Consulta para achar os usuários que assistiram o vídeo de maior duração
s6_sub1 = Selection('MAX(duracao)',
                    'VIDEOS',
                    '',
                    '',
                    '',
                    '')
s6 = Selection('nome',
               'VIDEOS NATURAL JOIN VISUALIZACOES NATURAL JOIN USUARIOS',
               f'duracao = ALL({createStringSelection(s6_sub1)})',
               '',
               '',
               '')

# Consulta todos os animes de mesma lista de Assistir Depois do usuário de id 325265 e mesmo gênero de Chainsaw Man de id 53153
s7_sub1_sub1 = Selection('DISTINCT nome_genero',
                         'CLASSIFICACOES_GENERO',
                         'anime_id = ANM.anime_id',
                         '',
                         '',
                         '')

s7_sub1 = Selection('nome_genero',
                    'CLASSIFICACOES_GENERO',
                    f'anime_id = 53153 AND nome_genero NOT IN ({createStringSelection(s7_sub1_sub1)})',
                    '',
                    '',
                    '')

s7_sub2_sub1 = Selection('user_id',
                         'ASSISTIRDEPOIS',
                         'anime_id = ANM.anime_id',
                         '',
                         '',
                         '')

s7_sub2 = Selection('user_id',
                    'ASSISTIRDEPOIS',
                    f'anime_id = 53153 AND user_id = 325265 AND user_id NOT IN ({createStringSelection(s7_sub2_sub1)})',
                    '',
                    '',
                    '')

s7 = Selection('ANM.nome',
               'ANIMES ANM',
               f'anime_id != 53153 AND NOT EXISTS ({createStringSelection(s7_sub1)}) AND NOT EXISTS ({createStringSelection(s7_sub2)})',
               '',
               '',
               '')

# Consulta para buscar histórico de um usuário durante a temporada Outono/22
s8 = Selection('nome, episodio, ts',
               'outono_2022 NATURAL JOIN VIDEOS NATURAL JOIN VISUALIZACOES',
               'user_id = 333985',
               '',
               '',
               'ts')

# Consulta para buscar os Shounens de Outono/22 dentro de uma determinada Crunchylista
s9 = Selection('nome, anime_id',
               'outono_2022 NATURAL JOIN CLASSIFICACOES_GENERO NATURAL JOIN INCLUSOES',
               "nome_genero = 'Shounen' AND crunchylista_id = 73364",
               '',
               '',
               '')

# Consulta para buscar todas visualizações
s10 = Selection('user_id, video_id, ts',
                'VISUALIZACOES',
                '',
                '',
                '',
                '')