import mysql.connector
from PySimpleGUI import *
from datetime import datetime,timedelta


filtro = ['Todos','Nome', 'Criador', 'Calorias']

import json
import os

# Caminho para o arquivo JSON que armazenará o tema
CAMINHO_JSON = 'tema_atual.json'
#########################################################   NUTROLOGO  #############################################################################################       NUTROLOGO        ##############################################################



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
    try:
        cursor.execute("SELECT id, nome, calorias_totais, criador, email  FROM dieta WHERE id_criador=%s AND apagado = nao AND em_branco = 'nao'",(id_criador,))
        dados = cursor.fetchall()

    except:
        dados =''
    finally:
                conn.close()
        
    return dados


def gerar_dados_estruturados(dados):
    
    tree_data = TreeData()
    for i, item in enumerate(dados):
        tree_data.insert("", int(item[0]), f"{item[0]}", item[1:])
    return tree_data


    
# Classe Livro para manipular os dados de livros
class Dieta:
    def __init__(self, id,nome,calorias_totais,criador,email,id_criador):
        self.id = id
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
            UPDATE dieta
            SET nome = %s, calorias_totais = %s, criador = %s, email= %s ,id_criador=%s,apagado = %s ,em_branco = %s
            WHERE id = %s
            ''', (self.nome, self.calorias,self.criador,self.email,self.id,'nao','nao',self.id))
            conn.commit()
            popup('Dieta adicionado com sucesso', title='Sucesso')
            
        except Exception as e:
            popup(f"Erro ao adicionar Dieta: {e}", title='Erro')
        finally:
            conn.close()

def fetch_books2(id_dieta):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Primeiro, busca todas as informações da tabela refeição
        cursor.execute("SELECT id, nome, horario, id_alimento, quantia,typo,preparo FROM refeiçao WHERE id_criador=%s AND apagado = 'nao'", (id_dieta,))
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
    except:
        refeicoes_com_nomes = []
    finally:
      conn.close()
    
    return refeicoes_com_nomes
    

def adicionar_alimento(nome,calorias,proteina,carboidratos,gorduras,typo_pesagem,quantia,id_criador):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
    
            cursor.execute('''
                INSERT INTO alimentos (nome,calorias,proteinas,carboidratos,gorduras,tipo_pesagem,id_criador,apagado,quantia)
                VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s)
            ''', (nome,calorias,proteina,carboidratos,gorduras,typo_pesagem,id_criador,'nao',quantia,))
            conn.commit()
            popup('alimento adicionado com sucesso', title='Sucesso')
        except Exception as e:
            popup(f"Erro ao adicionar alimento: {e}", title='Erro')
        finally:
            conn.close()
            
def fetch_books_4(id_):
    id_ =[id_]
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, calorias, proteinas, carboidratos,gorduras,tipo_pesagem, quantia  FROM alimentos WHERE apagado = 'nao' AND id_criador = %s",(id_))
    dados = cursor.fetchall()
    conn.close()
    return dados

def fetch_books_5(id_):
    id_ =[id_]
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, calorias, proteinas, carboidratos,gorduras,tipo_pesagem, quantia  FROM alimentos WHERE apagado = 'sim' AND id_criador = %s",(id_))
    dados = cursor.fetchall()
    conn.close()
    return dados

def restalrar_alimento(idl):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE alimentos
            SET apagado = %s
            WHERE id = %s
        """, ('nao', idl))
        conn.commit()
        popup('Alimento  restaurado  com sucesso', title='Sucesso')
    except Exception as e:
        popup(f"Erro ao restaurar o alimento : {e}", title='Erro')
    finally:
       conn.close()
       

def mover_alimento_para_apagados(id_alimento):
    data_atual = datetime.now()
    nova_data = data_atual + timedelta(days=15) 
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE alimentos
            SET apagado = %s, date = %s
            WHERE id = %s
          
        """, ('sim', nova_data, id_alimento))
        conn.commit()
        popup('Alimento movido para apagados com sucesso', title='Sucesso')
    except Exception as e:
        popup(f"Erro ao mover o alimento para apagados: {e}", title='Erro')
    finally:
       conn.close()
def apagar_alimento(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
          DELETE FROM alimentos id WHERE id = %s
          
        """, (id_alimento))
        conn.commit()
        popup('Alimento apagado com sucesso', title='Sucesso')
    except Exception as e:
        popup(f"Erro ao apagar o alimento: {e}", title='Erro')
    finally:
       conn.close()
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def tela_adicionar_alimento(id_):
    ty = ['gramas','ml']
    dados = fetch_books_4(id_)
    cabecalhos = ['Nome','Calorias','Proteinas', 'Carboidratos','Gorduras','Tipo de pesagem', 'Quantidade']
    tree_data = gerar_dados_estruturados(dados)
    return [[Text('Nome'),Input(key = 'nome')],
            [Text('Calorias'),Spin([i for i in range(0, 10000)], initial_value=1, key='calos')],
            [Text('Proteinas'),Spin([i for i in range(0, 10000)], initial_value=1, key='protes')],
            [Text('Caboidrados'),Spin([i for i in range(0, 10000)], initial_value=1, key='cabos')],
            [Text('Gorduras'),Spin([i for i in range(0, 10000)], initial_value=1, key='gordura')],
            [Text('Tipo de pesagem'),Combo(ty, default_value=ty[0], readonly=True, key='typo')],
            [Text('Quantia'),Spin([i for i in range(1, 1000)], initial_value=1, key='quantia')],
            [Button("Adicionar", font=("Arial", 12)), Button("Remover", font=("Arial", 12)),Button('Recuperar dados'),Button('Voltar')],
            [Tree(data=tree_data, headings=cabecalhos, col0_width=10, auto_size_columns=True, num_rows=10, key='-TREE-', show_expanded=False)],
            ]
    
    
    
def  rastrear_alimentos(id_criador):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM alimentos WHERE apagado = 'nao'AND  id_criador = %s ",(id_criador,))
    dados = cursor.fetchall()
    conn.close()
    nomes = [item[1] for item in dados]
    return dados
 
def  rastrear_alimento(id_criador):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM alimentos WHERE apagado = 'nao'AND  id_criador = %s ",(id_criador,))
    dados = cursor.fetchall()
    conn.close()

    return dados
 
 
def tela_restaurar_alimento(id_criador):
    dados = fetch_books_5(id_criador)  # Usando a função fetch_books para obter os livros
    cabecalhos = ['Nome','Calorias','Proteinas', 'Carboidratos','Gorduras','Tipo de pesagem', 'Quantidade']
    tree_data = gerar_dados_estruturados(dados)
    layout = [
    [Text('          Vida Saudavel começa com sua criaçao entao Crie e imagine', font=("Arial", 13))],
    [Button("Restaurar", font=("Arial", 12)), Button("Remover", font=("Arial", 12))],
    [Tree(data=tree_data, headings=cabecalhos, col0_width=10, auto_size_columns=True, num_rows=10, key='-TREE-', show_expanded=False)]
    ]
    return layout
    

def tela_inicial_nutrologo():
    return [
        [Menu([['Conta', ['Excluir conta','Tela']], ['Ajuda', ['Sobre']]])],
        [Text('           Menu')],
        [Button('Gerenciamento de dietas',key = 'dietas'),Button('Gerenciamento de conta', key='conta')],
        [Button('Adicionar alimento')]
      

    ]
def tela_EXCLUIR_conta():
    return[
        [Text('Tem certeza que quer excluir a conta')],
        [Button('Sim'),Button('Não')]
    ]


def Tela_adicionar_dieta(id_dieta,id_criador):
    dados = fetch_books2(id_dieta)  # Usando a função fetch_books para obter os livros
    cabecalhos = ['Nome','Calorias','Proteinas', 'Carboidratos','Gorduras','Tipo de pesagem', 'Quantidade','Descrisao']
    #ty = ['gramas','ml','kg','litro']
    ty = ['gramas','ml']
    tree_data = gerar_dados_estruturados(dados)
    alimentos = rastrear_alimentos(id_criador)
    layout = [
        [Button("Salvar", font=("Arial", 12)),Button("Voltar", font=("Arial", 12))],
        [Text('                                                                 Vida Saudavel começa com sua criaçao entao Crie e imagine', font=("Arial", 14))],
        [Text('Nome da Dieta '), Input(key='nome_dieta')],
        [Text('Nome do Criador '), Input(key='autor')],
        [Text('Email do criador'), Input(key='email')],
        [Text('       Adicione e gerencie as refeiçaoes abaixo:')],
        [Text('Nome da refeiçao'), Input(key='nome_refeiçao')],
        [Text('Horario da Refeiçao'), Input(key='localizacao')],
        [Text('Alimento'), Combo(alimentos, default_value=alimentos[0],enable_events= True, readonly=True, key='alimento')],
        [Text('Tipo '),InputText('', key='typo', disabled=True, size=(20, 1)),Text('Calorias'),InputText('', key='calorias', disabled=True, size=(20, 1)),Text('Proteinas'),InputText('', key='proteinas', disabled=True, size=(20, 1)),Text('Carboidratos'),InputText('', key='carboidratos', disabled=True, size=(20, 1)),Text('Gorduras'),InputText('', key='gorduras', disabled=True, size=(20, 1)),Text('Quantidade por esse valores'),InputText('', key='quantidade_', disabled=True, size=(20, 1))],
        [Text('Porçao'),  Spin([i for i in range(1, 100)], initial_value=1, key='quantia'),Text('Typo de pesagem para a refeiçao'), Combo(ty, default_value=ty[0], readonly=True, key='alimento')],
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





 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def apagar_refeiçao(id):
    conn = conectar_bd()
    if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM refeiçao WHERE  id = %s", (id,))
                conn.commit()
            except mysql.connector.Error as e:
                popup(f"Erro ao apagar a refeição: {e}")
            finally:
                cursor.close()
                conn.close()
    
def verificar_se_exste_branco():
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT  id, FROM dieta WHERE em_branco = 'sim'")
        dados = cursor.fetchone()
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
                cursor.execute("DELETE FROM refeiçao WHERE  id = %s", (id,))
                conn.commit()
                
        except mysql.connector.Error as e:
             pass
        finally:
            
                    cursor.close()
                    conn.close()
                    return None
    except:
        dados = None
    finally:
        conn.close()
        return dados
    
def criar_dieta_vasia():
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO dieta (em_branco)
                VALUES (%s)
            ''', ('sim',))  # Sem a vírgula após %s
            conn.commit()
            ultimo_id = cursor.lastrowid
            cursor.close()  # Fechar o cursor antes do return
            return ultimo_id

        except Exception as e:
            popup(f"Erro ao tentar abrir uma dieta: {e}", title='Erro')
            print(e)

        finally:
            cursor.close()

            conn.close()
def  excluir_conta(id_conta):
    data_atual = datetime.now()
    nova_data = data_atual + timedelta(days=15) 
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE dieta
            SET apagado = %s, date = %s
            WHERE id = %s
        """, ('sim', nova_data, id_conta))
        conn.commit()
        try:
          conn.close()
        except:
            pass
     
    except Exception as e:
        popup(f"Erro ao Tendar mover dieta para apagados: {e}", title='Erro')
        try:
          conn.close()
        except:
            pass
   
    else:
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE refeiçao
                SET apagado = %s, date = %s
                WHERE id_dieta = %s
            """, ('sim',nova_data, id_conta))
            conn.commit()

        except Exception as e:
            popup(f"Erro ao mover as refeiçaoes da dieta apagada para apagados: {e}", title='Erro')
        finally:
           conn.close()
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE alimentos
            SET apagado = %s, date = %s
            WHERE id_criador = %s
        """, ('sim', nova_data, id_criador))
        conn.commit()

    except Exception as e:
        popup(f"Erro ao mover o alimento para apagados: {e}", title='Erro')
    finally:
       conn.close()
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE usuario_dados
            SET apagado = %s, date = %s
            WHERE id = %s
        """, ('sim', nova_data, id_conta))
        conn.commit()
        try:
          conn.close()
        except:
            pass
     
    except Exception as e:
        popup(f"Erro ao Tendar mover dieta para apagados: {e}", title='Erro')
        try:
          conn.close()
        except:
            pass
    
    
                   
def mover_dieta_apagados(id):
    data_atual = datetime.now()
    nova_data = data_atual + timedelta(days=15) 
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE dieta
            SET apagado = %s, date = %s
            WHERE id = %s
        """, ('sim', nova_data, id))
        conn.commit()
        try:
          conn.close()
        except:
            pass
     
    except Exception as e:
        popup(f"Erro ao Tendar mover dieta para apagados: {e}", title='Erro')
        try:
          conn.close()
        except:
            pass
   
    else:
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE refeiçao
                SET apagado = %s, date = %s
                WHERE id_dieta = %s
            """, ('sim',nova_data, id))
            conn.commit()
            popup('Dieta movida para apados com sucesso ', title='Sucesso')
        except Exception as e:
            popup(f"Erro ao mover as refeiçaoes da dieta apagada para apagados: {e}", title='Erro')
        finally:
           conn.close()
    
def apaga_dieta(id):
    conn = conectar_bd()
    if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM dieta WHERE id_dieta = %s", (id,))
                conn.commit()
            except mysql.connector.Error as e:
                popup(f"Erro ao apagar o livro: {e}")
            finally:
                cursor.close()
                conn.close()
    conn = conectar_bd()
    if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM refeiçao WHERE id_dieta = %s", (id,))
                conn.commit()
                popup('Sucesso ao apagar os dados da dieta')
            except mysql.connector.Error as e:
                popup(f"Erro ao apagar a refeiçao da dieta: {e}")
            finally:
                cursor.close()
                conn.close()
def apagar_dieta():
    popup('Os dados de 15 dias atrás serão apagados automaticamente')
    data_limite = datetime.now().strftime("%Y-%m-%d")
    conn = conectar_bd()
    if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM dieta WHERE apagado =%s AND date <= %s", ('sim',data_limite))
                conn.commit()
        
            except mysql.connector.Error as e:
                popup(f"Erro ao apagar a dieta : {e}")
            finally:
                cursor.close()
                conn.close()
    conn = conectar_bd()
    if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM refeiçao WHERE  apagado =%s AND date <= %s", ('sim',data_limite))
                conn.commit()
            except mysql.connector.Error as e:
                popup(f"Erro ao apagar a refeição da dieta: {e}")
            finally:
                cursor.close()
                conn.close()


def restalrar_refeiçao(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE refeiçao
            SET apagado = %s
            WHERE id = %s
        """, ('nao', id))
        conn.commit()
        popup('Refeição  restaurada  com sucesso', title='Sucesso')
    except Exception as e:
        popup(f"Erro ao restaurar a  refeiçao : {e}", title='Erro')
    finally:
       conn.close()
       

def mover_refeiçao_para_apagados(id_refeiçao):
    data_atual = datetime.now()
    nova_data = data_atual + timedelta(days=15) 
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE refeiçao
            SET apagado = %s, date = %s
            WHERE id = %s
        """, ('sim', nova_data, id_refeiçao))
        conn.commit()
        popup('Refeição movida para apagados com sucesso', title='Sucesso')
    except Exception as e:
        popup(f"Erro ao mover refeiçao para apagados: {e}", title='Erro')
    finally:
       conn.close()
   
   
   
   
   
   
  #########################################################   NUTROLOGO  #############################################################################################       NUTROLOGO        ##############################################################
  
  
  
  

  
  
  
  #########################################################   LOGIN  #############################################################################################       LOGIN       ##############################################################
  

def salvar_tema(tema):
    with open(CAMINHO_JSON, 'w') as arquivo_json:
        json.dump({'tema': tema}, arquivo_json)

# Função que carrega o tema do arquivo JSON
def carregar_tema():
    if os.path.exists(CAMINHO_JSON):
        with open(CAMINHO_JSON, 'r') as arquivo_json:
            dados = json.load(arquivo_json)
            return dados.get('tema', theme())  # Retorna o tema salvo ou o padrão se não existir
    return theme()

def verificar_usuario(user):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Verificar a existência do usuário, assumindo que 'apagados' é do tipo VARCHAR e usamos 'nao'
        cursor.execute('''
            SELECT id, nome,email, user, senha, tipo, id_dieta 
            FROM usuario_dados 
            WHERE user = %s AND apagado = 'nao'
        ''', (user,))
    except Exception as e:
        # Se houver erro, exibe o popup e retorna None
        popup(f'Erro ao conectar com banco de dados: {str(e)}', title='Erro')
        dados = None
    else:
        dados = cursor.fetchall()  # Captura os resultados da query
        if dados:  # Verifica se algum dado foi encontrado
            return dados
        else:
            return None  # Retorna None se não encontrar nenhum usuário
    finally:
        conn.close()  # Garante que a conexão seja fechada

def adicionar_usuario(nome, email,user,senha,tipo):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuario_dados (nome, email,user,senha,tipo,apagado)
                VALUES (%s,%s,%s,%s,%s,%s)
            ''', (nome, email,user,senha,tipo,'nao'))
            conn.commit()
            ultimo_id = cursor.lastrowid
            return ultimo_id
            cursor.close()
       
        except Exception as e:
            popup(f"Erro : {e}", title='Erro')
        
        else:
                                 popup('Usuario cadastrado com sucesso')
        finally:

            conn.close()
         
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   

def tela_login():
    return[
        [Menu([['Ajuda',['Restaurar conta','Recuperar senha']],['Sobre',['Empresa: Wel Combani','Numero: 40028922']]])],
        [Text('Usuario')],
        [Input(key='-nome-')],
        [Text('Senha')],
        [Input(key='-senha-', password_char='*', enable_events=True)],
        [Button('OK'), Button('Cancelar'), Button('Cadastrar')]
        
        
    ]
  
def tela_cadastro():
      return [
        [Text('Nome')],
        [Input(key = 'nome')],
        [ Text('Email')],
        [ Input(key='email')],
        [Text('User')],
        [Input(key = 'user')],
        [ Text('Senha')],
        [ Input(key='-senha-', password_char='*')],
        [ Text('Repetir Senha')],
        [ Input(key='-senha_rep-', password_char='*')],
        [ Radio("Usuario", "1", default=True, key='Usuario'),Radio("Nutrologo", '1', key='Nutrólogo')],
        [ Button('Cadastrar'), Button('Cancelar')]
    ]
    
  
  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
  
  
  
  
  
  
 
 
 
 
 
 #########################################################   LOGIN  #############################################################################################       LOGIN         ##############################################################
  
 
 

 
 
 
 
 
 
 
 
def criar_janela_tema_atual(tema_atual):
    theme(tema_atual)  # Define o tema atual
    
    layout = [
        [Text(f'Tema atual: {tema_atual}', font=("Helvetica", 16))],
        [Text('Selecione um tema da lista abaixo:')],
        [Listbox(values=theme_list(), size=(30, 10), key='-LIST-', enable_events=True)],
        [Button('Sair')]
    ]
    
    return Window(f'Tema: {tema_atual}', layout, finalize=True)
 
 
 
 
 
  #########################################################    USUARIO  #############################################################################################         USUARIO         ##############################################################
  
  
















def fetch_books_3():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, calorias_totais, criador, email  FROM dieta WHERE apagado = nao AND em_branco = nao")
    dados = cursor.fetchall()
    conn.close()
    return dados

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



def tela_inicial_usuario():
    return [
        [Menu(['Conta', ['Excluir conta '], ['Ajuda', ['Sobre']]])]
        [Text('           Menu')],
        [Button('Dietas catalogo',key = 'dietas'),Button('Dieta', key='conta')],
        [Button('Chat com criador ')]
      

    ]

def tela_dietas():

    dados = fetch_books_3()  # Usando a função fetch_books para obter os livros
    cabecalhos = ['Nome','Calorias da Dieta', 'Criador', 'Email']
    tree_data = gerar_dados_estruturados(dados)
    layout = [
    [Text('          Vida Saudavel começa com sua escolha e percistencia', font=("Arial", 13))],
    [Button("Salvar dieta", font=("Arial", 12)), Button("Ver dieta", font=("Arial", 12))],
    [Tree(data=tree_data, headings=cabecalhos, col0_width=10, auto_size_columns=True, num_rows=10, key='-TREE-', show_expanded=False)]
    ]
    return layout


def ver_refeiçao_em_dieta(id_dieta):
    pass
    



    # Adicionar a coluna com rolagem horizontal e vertical
 
    
    


    




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 








def calcular_nutrientes(quantia, tipo_pesagem, calorias, proteinas, carboidratos, gorduras):
    fator = quantia / 100 if tipo_pesagem == "gramas" or tipo_pesagem == "ml" else quantia
    calorias_ajustadas = calorias * fator
    proteinas_ajustadas = proteinas * fator
    carboidratos_ajustados = carboidratos * fator
    gorduras_ajustadas = gorduras * fator
    return calorias_ajustadas, proteinas_ajustadas, carboidratos_ajustados, gorduras_ajustadas

# Função para buscar os dados da dieta e refeições no banco de dados
def pegar_dados_dieta(id_dieta):
    conn = conectar_bd()
    cursor = conn.cursor()

    # Consulta a dieta na tabela dieta
    cursor.execute("SELECT id, nome,calorias_totais, criador, email FROM dieta WHERE id = %s AND apagado = 'nao'", (id_dieta,))
    dados_dieta = cursor.fetchone()

    if not dados_dieta:
        conn.close()
        return None  # Retorna None se não encontrar a dieta

    # Consulta as refeições relacionadas à dieta
    cursor.execute("SELECT id, nome, horario, id_alimento, quantia, typo, preparo FROM refeiçao WHERE id_dieta = %s AND apagado = 'nao'", (id_dieta,))
    refeicoes = cursor.fetchall()

    # Lista para armazenar as informações estruturadas
    lista_alimentos = []

    # Processar cada refeição
    for refeicao in refeicoes:
        id_refeicao, nome_refeicao, horario, id_alimento, quantia, typo_pesagem, preparo = refeicao

        # Buscar o nome e informações nutricionais do alimento correspondente
        cursor.execute("SELECT nome, calorias, proteinas, carboidratos, gorduras, tipo_pesagem FROM alimentos WHERE id = %s", (id_alimento,))
        alimento_info = cursor.fetchone()

        if alimento_info:
            nome_alimento, calorias, proteinas, carboidratos, gorduras, tipo_pesagem_alimento = alimento_info

            # Calcular os nutrientes ajustados de acordo com a quantia e tipo de pesagem
            calorias_ajustadas, proteinas_ajustadas, carboidratos_ajustados, gorduras_ajustadas = calcular_nutrientes(
                quantia, typo_pesagem, calorias, proteinas, carboidratos, gorduras
            )

            # Estruturar os dados em um dicionário
            alimento_dict = {
                'nome': nome_alimento,
                'horario': horario,
                'calorias': calorias_ajustadas,
                'proteinas': proteinas_ajustadas,
                'carboidratos': carboidratos_ajustados,
                'gorduras': gorduras_ajustadas,
                'quantia': quantia,  # Inclui a quantia aqui
                'tipo_pesagem': typo_pesagem,
                'preparo': preparo
            }

            # Adicionar à lista de alimentos
            lista_alimentos.append(alimento_dict)

    conn.close()

    # Retornar os dados da dieta e a lista de alimentos processada
    return {
        'nome_dieta': dados_dieta[1],
        'calorias_t': dados_dieta[2],
        'criador':dados_dieta[3],
        'email': dados_dieta[4],
        'alimentos': lista_alimentos
    }

# Função para mostrar os dados da dieta no PySimpleGUI
def mostrar_dieta(id_dieta):
    # Pegar os dados da dieta e das refeições
    dados_dieta = pegar_dados_dieta(id_dieta)

    if not dados_dieta:
        popup('Dieta não encontrada!', title='Erro')
        return

    # Dados da dieta
    nome_dieta = dados_dieta['nome_dieta']
    criador = dados_dieta['criador']
    email = dados_dieta['email']
    refeicoes = dados_dieta['alimentos']  # Lista de refeições e nutrientes
    calorias_t = 1

    # Layout principal com informações da dieta
    layout = [
        [Button('Voltar')],
        [Text('Dieta: ' + nome_dieta, font=("Arial", 20), justification='center')],
        [Text('Criador: ' + criador, font=("Arial", 16), justification='center')],
        [Text('Email: ' + email, font=("Arial", 16), justification='center')],
        [Text('Calorias totais: ' + calorias_t, font=("Arial", 16), justification='center')]
        [Text('--- Refeições ---', font=("Arial", 18), justification='center', pad=(0, 20))]
    ]

    # Layout de refeições a ser adicionado na coluna rolável
    refeicoes_layout = []
    for refeicao in refeicoes:
        refeicoes_layout.append([Text(f"Refeição: {refeicao['nome']}", font=("Arial", 14))])
        refeicoes_layout.append([Text(f"Horário: {refeicao['horario']}", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Alimento: {refeicao['nome']}", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Calorias: {refeicao['calorias']:.2f} Kcal", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Proteínas: {refeicao['proteinas']:.2f} g", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Carboidratos: {refeicao['carboidratos']:.2f} g", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Gorduras: {refeicao['gorduras']:.2f} g", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Quantia: {refeicao['quantia']} {refeicao['tipo_pesagem']}", font=("Arial", 12))])  # Mostra quantia
        refeicoes_layout.append([Text(f"Preparo: {refeicao['preparo']}", font=("Arial", 12))])
        refeicoes_layout.append([Text('---------------------------------------------', font=("Arial", 12))])

    # Adicionar a coluna com rolagem vertical
    layout.append(
        [Column(refeicoes_layout, size=(800, 400), scrollable=True, vertical_scroll_only=True)]
    )

    # Criação da janela com tela cheia
    window = Window('Detalhes da Dieta', layout, finalize=True, resizable=True, size=(1920, 1080))

    # Loop de eventos da janela
    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == 'Voltar':
            break

    window.close()

def escolher_dieta_mostrar():
 # Pegar os dados da dieta e das refeições
    dados_dieta = pegar_dados_dieta(id_dieta)

    if not dados_dieta:
        popup('Dieta não encontrada!', title='Erro')
        return

    # Dados da dieta
    nome_dieta = dados_dieta['nome_dieta']
    criador = dados_dieta['criador']
    email = dados_dieta['email']
    refeicoes = dados_dieta['alimentos']  # Lista de refeições e nutrientes
    calorias_t = 1

    # Layout principal com informações da dieta
    layout = [
        [Button('Voltar'),Button('Salvar')],
        [Text('Dieta: ' + nome_dieta, font=("Arial", 20), justification='center')],
        [Text('Criador: ' + criador, font=("Arial", 16), justification='center')],
        [Text('Email: ' + email, font=("Arial", 16), justification='center')],
        [Text('Calorias totais: ' + calorias_t, font=("Arial", 16), justification='center')]
        [Text('--- Refeições ---', font=("Arial", 18), justification='center', pad=(0, 20))]
    ]

    # Layout de refeições a ser adicionado na coluna rolável
    refeicoes_layout = []
    for refeicao in refeicoes:
        refeicoes_layout.append([Text(f"Refeição: {refeicao['nome']}", font=("Arial", 14))])
        refeicoes_layout.append([Text(f"Horário: {refeicao['horario']}", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Alimento: {refeicao['nome']}", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Calorias: {refeicao['calorias']:.2f} Kcal", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Proteínas: {refeicao['proteinas']:.2f} g", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Carboidratos: {refeicao['carboidratos']:.2f} g", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Gorduras: {refeicao['gorduras']:.2f} g", font=("Arial", 12))])
        refeicoes_layout.append([Text(f"Quantia: {refeicao['quantia']} {refeicao['tipo_pesagem']}", font=("Arial", 12))])  # Mostra quantia
        refeicoes_layout.append([Text(f"Preparo: {refeicao['preparo']}", font=("Arial", 12))])
        refeicoes_layout.append([Text('---------------------------------------------', font=("Arial", 12))])

    # Adicionar a coluna com rolagem vertical
    layout.append(
        [Column(refeicoes_layout, size=(800, 400), scrollable=True, vertical_scroll_only=True)]
    )

    # Criação da janela com tela cheia
    window = Window('Detalhes da Dieta', layout, finalize=True, resizable=True, size=(1920, 1080))

    # Loop de eventos da janela
    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == 'Voltar':
            break

    window.close()









 
#########################################################    USUARIO  #############################################################################################         USUARIO         ##############################################################



















#########################################################    CODE    #############################################################################################         CODE       ##############################################################
 

tema_atual = carregar_tema()
theme(tema_atual)

janela = Window('Login',tela_login())


while True:
    
    evento,valor = janela.read()
    if evento == 'Cancelar' or evento == WIN_CLOSED:
        break
    if evento == 'Cadastrar':
        janela.close()
        janela = Window('Cadastro',tela_cadastro())
        while True:
             evento,valor =  janela.read()
             if evento == 'Cancelar'or evento  == WIN_CLOSED:
                 janela.close()
                 janela = Window('Login',tela_login())
                 break
             if evento == 'Cadastrar':
                if not valor['nome'] or not valor['email'] or not valor['-senha-'] or not valor['-senha_rep-']:
                    popup('Preencha todos os campos')
                else:
                    if valor['-senha-'] == valor['-senha_rep-']:
                        a = verificar_usuario(valor['user'])
                        if not a:  # A função agora retorna None se o usuário não for encontrado
                             typo = 'Usuario' if valor['Usuario'] else 'Nutrólogo'
                             adicionar_usuario(valor['nome'], valor['email'], valor['user'], valor['-senha-'], typo)
                             janela.close()
                             janela = Window('Login',tela_login())
                             popup(F'Adicionado com sucesso o {typo}')
                             break
                        else:
                            popup('Usuário existente')
                    else:
                        popup('As senhas não coincidem')
                              
    if evento == 'OK':
        if not valor['-nome-'] or not valor['-senha-']:
            popup('Preencha todos os campos')
        else:
        
           try:
            a =  verificar_usuario(valor['-nome-'])
            a = a[0]
           except:
              a = None
           if not a :
               popup('O usuario não existe')
           else: 
               if a[4] == valor['-senha-']:
                   if a[5] == 'Nutrólogo':
                       dados_user = a 
                       janela.close()
                       janela = Window('Menu nutrólogo',tela_inicial_nutrologo())
                       while True:
                           evento,valor = janela.read()
                           if evento  == WIN_CLOSED:
                                 janela.close()
                                 janela = Window('Login',tela_login())
                                 break
                                 
                           if evento =='dietas' or evento == "Gerenciamento de dietas":
                               janela.close()
                         
                               janela =Window('Adicionar dieta',tela_dieta(dados_user[0]))
                               while True :
                                   evento,valor = janela.read()
                                   if evento  == WIN_CLOSED:
                                         janela.close()
                                         janela = Window('Menu nutrólogo',tela_inicial_nutrologo())
                                         break
                                   if evento == 'Remover':
                                       pass
                                   if evento == 'Recuperar dados':
                                       pass
                                   if evento == 'Alterar':
                                       pass
                                   if evento == 'Adicionar':
                                       dado = verificar_se_exste_branco()
                                       if not dado:
                                           id_dieta = criar_dieta_vasia()
                                           janela.close()
                                           janela = Window('Adicionar dieta',Tela_adicionar_dieta(id_dieta,dados_user[0]))
                                           a = ''
                                           while True:
                                                evento,valor = janela.read()
                                                if evento  == WIN_CLOSED:
                                                    janela.close()
                                                    janela = Window('Adicionar dieta',tela_dieta(dados_user[0]))
                                                    break
                                                if evento == "Adicionar":
                                                    if not valor[''] and 
                                                    
                                                if valor['alimento'] != a:
                                                    
                                                        id_selecionado = valor['alimento'][0]  # Pega o primeiro elemento da tupla (ID)

                                               

                                                        # Continua se o id_selecionado foi encontrado
                                                        if id_selecionado:
                                                            conn = conectar_bd()
                                                            cursor = conn.cursor()
                                                            cursor.execute("SELECT id, nome, calorias, proteinas, carboidratos, gorduras, tipo_pesagem, quantia FROM alimentos WHERE id = %s", (id_selecionado,))
                                                            dados = cursor.fetchone()
                                                            conn.close()
                                                            
                                                            if dados:
                                                                janela['typo'].update(dados[5], disabled=True)
                                                                janela['calorias'].update(dados[2], disabled=True)
                                                                janela['proteinas'].update(dados[3], disabled=True)
                                                                janela['carboidratos'].update(dados[4], disabled=True)
                                                                janela['gorduras'].update(dados[5], disabled=True)
                                                                janela['quantidade_'].update(dados[6])

                                                            a = valor['alimento']
                                                                                
                                                
                                        
                                                    
                                        
                                               
                           
                           if evento == 'Excluir conta':
                               janela.close()
                               janela = Window('Excluir conta',tela_EXCLUIR_conta())
                               while True:
                                    evento,valor = janela.read()
                                    if evento == 'Não' or evento  == WIN_CLOSED:
                                        janela.close()
                                        janela = Window('Login',tela_inicial_nutrologo())
                                        break
                                    if evento == 'Sim':
                                        excluir_conta(dados_user[0])
                                        janela.close()
                                        janela = Window('Login',tela_login())
                                   
                                    
                           if evento == 'Tela':
                                janela.close()
                                tema_atual = carregar_tema()
                                janela = criar_janela_tema_atual(tema_atual)
                                while True:
                                    evento, valores = janela.read()

                                    if evento == WIN_CLOSED or evento == 'Sair':
                                       janela.close()
                                       janela = Window('Menu nutrólogo',tela_inicial_nutrologo())
                                       break

             
                                    if evento == '-LIST-':
                                        novo_tema = valores['-LIST-'][0] 
                                        janela.close()  
                                        salvar_tema(novo_tema)  # Salva o novo tema em JSON
                                        janela = criar_janela_tema_atual(novo_tema)  
                           
                           
                           
                           if evento == 'Adicionar alimento':
                               janela.close()
                               janela = Window('Adicionar',tela_adicionar_alimento(dados_user[0]))
                               while True:
                                   evento,valor = janela.read()
                                   if evento == 'Voltar' or evento == WIN_CLOSED:
                                       janela.close()
                                       janela = Window('Login',tela_inicial_nutrologo())     
                                       break
                                   if evento == 'Adicionar':
                                        if not valor['nome']or   not valor['quantia']:  
                                           popup('preencha todos os campos')
                                        else:
                                            adicionar_alimento(valor['nome'],valor['calos'],valor['protes'],valor['cabos'],valor['gordura'],valor['typo'],valor['quantia'],dados_user[0])
                                            janela['-TREE-'].update(values=gerar_dados_estruturados(fetch_books_4(dados_user[0])))
                                            
                                            janela['nome'].update('')
                                            janela['calos'].update(0)
                                            janela['protes'].update(0)
                                            janela['cabos'].update(0)
                                            janela['gordura'].update(0)
                                            janela['quantia'].update(1)
                                            
                                   if evento == 'Remover':
                                        selecionado = valor['-TREE-']
                                        if selecionado:
                                            id_alimento = selecionado[0]
                                            mover_alimento_para_apagados(id_alimento)
                                            janela['-TREE-'].update(values=gerar_dados_estruturados(fetch_books_4(dados_user[0])))
                                   if evento ==  'Recuperar dados':
                                       janela.close()
                                       janela = Window('restaurar refeiçao', tela_restaurar_alimento(dados_user[0]))
                                       while True:
                                           evento,valor = janela.read()
                                           if evento  == WIN_CLOSED:
                                                  janela.close()
                                                  janela = Window('Adicionar',tela_adicionar_alimento(dados_user[0]))
                                                  break
                                           if evento == 'Restaurar':
                                                selecionado = valor['-TREE-']
                                                if selecionado:
                                                    id_alimento = selecionado[0]
                                                    restalrar_alimento(int(id_alimento))
                                                    janela['-TREE-'].update(values=gerar_dados_estruturados(fetch_books_5(dados_user[0])))
                                           if evento == 'Remover':
                                                selecionado = valor['-TREE-']
                                                if selecionado:
                                                      id_alimento = selecionado[0]
                                                      id_alimento = [id_alimento]
                                                      apagar_alimento(id_alimento)
                                                      
                                                      janela['-TREE-'].update(values=gerar_dados_estruturados(fetch_books_5(dados_user[0])))
                                                    
                                               
                                                    
                                                
                                            
                                       
                                           
                                            
                               
                       
                       
                    
                    
                    
                    
                   elif a[5] =='Usuario':
                       pass
                       
                       
                       
                       
                       
                   else:
                       popup('Erro no sistema')
                   
                   
               else:
                   popup('A senha ou usuario esta errada ')

janela.close()   
























