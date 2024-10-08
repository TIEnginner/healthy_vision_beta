import mysql.connector
from PySimpleGUI import *
from datetime import datetime,timedelta


filtro = ['Todos','Nome', 'Criador', 'Calorias']


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
    cursor.execute("SELECT id, nome, calorias_totais, criador, email  FROM dieta WHERE id_criador=%s AND apagado = nao AND em_branco = nao",(id_criador,))
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
    

def adicionar_refeiçao(nome,calorias,proteina,carboidratos,gorduras,typo_pesagem):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO refeiçao ()
                VALUES (%s, %s, %s, %s,%s,%s,%s)
            ''', (nome,calorias,proteina,carboidratos,gorduras,typo_pesagem,'nao'))
            conn.commit()
            popup('Refeição adicionado com sucesso', title='Sucesso')
        except Exception as e:
            popup(f"Erro ao adicionar refeição: {e}", title='Erro')
        finally:
            conn.close()
 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def tela_inicial_nutrologo():
    return [
        [Menu(['Conta', ['Excluir conta '], ['Ajuda', ['Sobre']]])]
        [Text('           Menu')],
        [Button('Gerenciamento de dietas',key = 'dietas'),Button('Gerenciamento de conta', key='conta')],
        [Button('Abrir loja')]
      

    ]
def tela_EXCLUIR_conta():
    return[
        [Text('Tem certeza que quer excluir a conta')],
        [Button('Sim'),Button('Não')]
    ]


def Tela_adicionar_dieta(id_dieta):
    dados = fetch_books2(id_dieta)  # Usando a função fetch_books para obter os livros
    cabecalhos = ['Nome do alimento ','Horario da refeiçao ', 'Alimento', 'Porçao']
    tree_data = gerar_dados_estruturados(dados)
    alimentos = ['mamao']
    layout = [
        [Button("Salvar", font=("Arial", 12)),Button("Voltar", font=("Arial", 12))],
        [Text('                                                                 Vida Saudavel começa com sua criaçao entao Crie e imagine', font=("Arial", 14))],
        [Text('Nome da Dieta '), Input(key='nome_dieta')],
        [Text('Nome do Criador '), Input(key='autor')],
        [Text('Email do criador'), Input(key='email')],
        [Text('       Adicione e gerencie as refeiçaoes abaixo:')]
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





 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def apagar_refeiçao(id):
    conn = conectar_bd()
    if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM refeiçao WHERE  id", (id,))
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
        cursor.execute("SELECT  id, FROM dieta WHERE em_branco = %s", ('sim',))
        dados = cursor.fetchone()
    except:
        popup('Erro inesperado')
        dados = ''
    finally:
        conn.close()
        return dados
    
def criar_dieta_vasia():
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO dieta (em_branco)
                VALUES (%s,)
            ''', ('sim'))
            conn.commit()
            ultimo_id = cursor.lastrowid
            return ultimo_id
            cursor.close()

        except Exception as e:
            popup(f"Erro ao tendar abrir uma dieta: {e}", title='Erro')
        finally:

            conn.close()
def  excluir_conta():
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
  

  

def verificar_usuario(user):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
      cursor.execute('''
           SELECT  id,email,user,senha,tipo,id_dieta FROM usuario_dados WHERE user  = %s AND apagados = nao ''',(user,))
    
    except Exception as e:
        popup('Erro ao conectar com banco de dados da Wel Combani',title = 'Erro')
        dados =''
    else:
        dados = cursor.fetchall()
        return dados
        
    finally:
            conn.close()

def adicionar_usuario(nome, email,user,senha,tipo):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuario_dados (nome, email,user,senha,tipo,apagados)
                VALUES (%s,%s,%s,%s,%s,%s)
            ''', (nome, email,user,senha,tipo,'nao'))
            conn.commit()
            ultimo_id = cursor.lastrowid
            return ultimo_id
            cursor.close()

        except Exception as e:
            popup(f"Erro ao tendar abrir uma dieta: {e}", title='Erro')
        finally:

            conn.close()
         
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   

def tela_login():
    return[
        [Menu(['Ajuda',['Restaurar conta','Recuperar senha']])],
        [Text('Usuario')],
        [Input(key='-nome-')],
        [Text('Senha')],
        [Input(key='-senha-', password_char='*', enable_events=True)],
        [Button('OK'), Button('Cancelar'), Button('Cadastrar')]
        
        
    ]
  
def tela_cadastro():
      return [
        [Text('Nome')],
        [Input(key = 'nome')]
        [ Text('Email')],
        [ Input(key='email')],
        [Text('User')]
        [Input(key = 'user')]
        [ Text('Senha')],
        [ Input(key='-senha-', password_char='*')],
        [ Text('Repetir Senha')],
        [ Input(key='-senha_rep-', password_char='*')],
        [ Radio("Usuario", "1", default=True, key='Usuario'),Radio("Nutrologo", '1', key='Nutrólogo')],
        [ Button('Cadastrar'), Button('Cancelar')]
    ]
    
  
  
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
  
  
  
  
  
  
 
 
 
 
 
 #########################################################   LOGIN  #############################################################################################       LOGIN         ##############################################################
  
 
 

 
 
 
 
 
 
 
 
 
 
 
 
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


def ver_refeiçao_em_dieta():
    pass
    
def tela_dieta():
    pass




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



def extruturar_dieta(id):
    pass











 
#########################################################    USUARIO  #############################################################################################         USUARIO         ##############################################################



















#########################################################    CODE    #############################################################################################         CODE       ##############################################################
 



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
                 if not valor['nome']and not valor['email']and not valor['-senha-']and not valor['-senha_rep-']:
                     popup('Preencha todos os campos')
                 else:
                          if valor['-senha-'] == valor['-senha_rep-']:
                              a =  verificar_usuario(valor['user'])
                              if not a or a  =='':
                                  if valor['Usuario']:
                                      typo = 'Usuario'
                                  else:
                                      typo ='Nutrólogo'
                                  adicionar_usuario(valor['nome'],valor ['email'],valor['user'],valor['senha'],typo)
                                  popup('Usuario cadastrado com sucesso')
                              else:
                                  popup('Usuario existende')
                          else:
                              popup('as senhas nao coincidem')
                              
    if evento == 'Ok':
        if not valor['-nome-'] or not valor['-senha-']:
            popup('Preencha todos os campos')
        else:
           a =  verificar_usuario(valor['nome'])
           if not a and a =='':
               popup('O usuario não existe')
           else: 
               if a[3] == valor['-senha-'] and a[2]== valor['-nome-']:
                   if 
                   
               else:
                   popup('A senha ou usuario esta errada ')

    
























