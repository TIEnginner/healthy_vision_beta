import mysql.connector
from PySimpleGUI import *
from datetime import datetime,timedelta


filtro = ['Todos','Nome', 'Criador', 'Calorias']

# Conexão com o banco de dados MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="acesso123",
        database="projeto_dieta"
    )

# Função para buscar todos os livros no banco de dados
def fetch_books(id_criador):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, calorias_totais, criador, email  FROM dieta WHERE id_criador=%s AND apagado = nao",(id_criador,))
    dados = cursor.fetchall()
    conn.close()
    return dados


def gerar_dados_estruturados(dados):
    tree_data = TreeData()
    for i, item in enumerate(dados):
        tree_data.insert("", int(item[0]), f"{item[0]}", item[1:])
    return tree_data

# Classe Livro para manipular os dados de livros
class Dieta:
    def __init__(self, nome,calorias_totais,criador,email,id_criador):
        self.nome = str(nome)
        self.calorias = str(calorias_totais) + 'Kcal'
        self.criador =  criador
        self.email =  email
        self.id = id_criador
      
    
    def adicionar(self):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO dieta (nome, calorias_totais, criador, email,id_criador,apagado)
                VALUES (%s, %s, %s, %s,%s,%s)
            ''', (self.nome, self.calorias,self.criador,self.email,self.id,'nao'))
            conn.commit()
            popup('Dieta adicionado com sucesso', title='Sucesso')
        except Exception as e:
            popup(f"Erro ao adicionar Dieta: {e}", title='Erro')
        finally:
            conn.close()

def fetch_books2(id_dieta):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Primeiro, busca todas as informações da tabela refeição
    cursor.execute("SELECT id, nome, horario, id_alimento, quantia FROM refeiçao WHERE id_criador=%s AND apagado = nao", (id_dieta,))
    dados_refeicoes = cursor.fetchall()
    
    refeicoes_com_nomes = []
    
    for refeicao in dados_refeicoes:
        id_alimento = refeicao[3]
        
        # Para cada refeição, buscamos o nome do alimento correspondente ao id_alimento
        cursor.execute("SELECT nome FROM alimentos WHERE id=%s", (id_alimento,))
        alimento = cursor.fetchone()
        
        # Substitui o id_alimento pelo nome do alimento
        if alimento:
            refeicao = list(refeicao)  # Converter para lista para ser mutável
            refeicao[3] = alimento[0]  # Substitui o id_alimento pelo nome do alimento
            refeicoes_com_nomes.append(tuple(refeicao))  # Converter de volta para tupla

    conn.close()
    
    return refeicoes_com_nomes
    



def Tela_adicionar_dieta(id_dieta):
    dados = fetch_books2(id_dieta)  # Usando a função fetch_books para obter os livros
    cabecalhos = ['Nome do aLimento ','Horario da refeiçao ', 'Alimento', 'Porçao']
    tree_data = gerar_dados_estruturados(dados)
    alimentos = ['mamao']
    layout = [
       
        [Text('Nome da Dieta '), Input(key='nome_dieta')],
        [Text('Nome do Criador '), Input(key='autor')],
        [Text('Email do criador'), Input(key='email')],
        [Text('Nome da refeiçao'), Input(key='nome_refeiçao')],
        [Text('Horario da Refeiçao'), Input(key='localizacao')],
        [Text('Alimento'), Combo(alimentos, default_value=alimentos[0], readonly=True, key='idioma')],
        [Text('Tipo'),InputText('', key='typo', disabled=True, size=(30, 1)),Text('Calorias'),InputText('', key='calorias', disabled=True, size=(30, 1)),Text('Proteinas'),InputText('', key='proteinas', disabled=True, size=(30, 1)),Text('Carboidratos'),InputText('', key='carboidratos', disabled=True, size=(30, 1)),Text('Gorduras'),InputText('', key='gorduras', disabled=True, size=(30, 1))]
        [Text('Peso ou quantidade'), Input(key='')],
        [Text('Descriçao ou  preparo')],
        [Multiline(size=(30, 5), key='textbox')],
        [Button("Adicionar", font=("Arial", 12)), Button("Remover", font=("Arial", 12)), Button("Alterar", font=("Arial", 12)), Button('Recuperar dados', font=("Arial", 12))],
        [Tree(data=tree_data, headings=cabecalhos, col0_width=10, auto_size_columns=True, num_rows=10, key='-TREE-', show_expanded=False)]
    ]
    return layout

def tela_dieta(id_criador):
    dados = fetch_books(id_criador)  # Usando a função fetch_books para obter os livros
    cabecalhos = ['Nome','Calorias da Dieta', 'Criador', 'Email']
    tree_data = gerar_dados_estruturados(dados)
    layout = [
    [Text('          Vida Saudavel começa com sua criaçao entao Crie e imagine', font=("Arial", 13))],
    [Button("Adicionar", font=("Arial", 12)), Button("Remover", font=("Arial", 12)), Button("Alterar", font=("Arial", 12)), Button('Recuperar dados', font=("Arial", 12))],
    [Tree(data=tree_data, headings=cabecalhos, col0_width=10, auto_size_columns=True, num_rows=10, key='-TREE-', show_expanded=False)]
    ]
    return layout

