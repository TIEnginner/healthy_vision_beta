import flet as ft
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Cria uma conexão com o banco de dados MySQL."""
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="acesso123",
            database="diets"
        )
        print("Conexão bem-sucedida!")
        return connection
    except Error as e:
        print(f"Ocorreu um erro: {e}")
        return None

def verify_user(nome, senha):
    """Verifica se o usuário existe no banco de dados."""
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome, senha))
                return cursor.fetchone() is not None
        except Error as e:
            print(f"Ocorreu um erro ao verificar usuário: {e}")
        finally:
            conn.close()
    return False

def menu(page: ft.Page):
    page.title = "Acompanhamento de dietas"
    page.theme = ft.Theme(color_scheme_seed='yellow')
    page.add(ft.Text(value='Bem vindo!', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK))
    
    radio_group = ft.RadioGroup(
        value='Nutrólogo',
        content=ft.Column(
            controls=[
                ft.Radio(value="Nutrólogo", label="Nutrólogo"),
                ft.Radio(value='Paciente', label='Paciente')
            ]
        )
    )
    
    name_field = ft.TextField(label='Nome:', text_align=ft.TextAlign.LEFT)
    password_field = ft.TextField(label='Senha:', password=True, text_align=ft.TextAlign.LEFT)

    def add_medic(e):
        global R, P, E
        R = ft.TextField(label="Digite seu nome:", text_align=ft.TextAlign.LEFT)
        P = ft.TextField(label='Digite sua senha:', password=True, text_align=ft.TextAlign.LEFT)
        E = ft.TextField(label='Digite seu email:', text_align=ft.TextAlign.LEFT)

        dialog = ft.AlertDialog(
            title=ft.Text("Cadastro de nutrólogo"),
            content=ft.Column([R, P, E]),
            actions=[ft.ElevatedButton(text='Cadastrar nutrólogo', on_click=doctor_registration)],
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def add_pacient(e):
        global T, W, S
        T = ft.TextField(label='Digite seu nome:', text_align=ft.TextAlign.LEFT)
        W = ft.TextField(label='Digite seu email:', text_align=ft.TextAlign.LEFT)
        S = ft.TextField(label='Digite sua senha:', password=True, text_align=ft.TextAlign.LEFT)

        dialogo = ft.AlertDialog(
            title=ft.Text("Cadastro de paciente"),
            content=ft.Column([T, W, S]),
            actions=[ft.ElevatedButton(text='Cadastrar paciente', on_click=pacient_registration)],
        )

        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def warning_error():
        popup = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text("Não foi possível encontrar o usuário, verifique as informações e tente novamente.")
        )
        page.dialog = popup
        popup.open = True
        page.update()

    def on_send_click(e):
        nome = name_field.value.strip()
        senha = password_field.value.strip()

        if not nome or not senha:
            snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
            page.snack_bar = snack_bar
            snack_bar.open = True
            page.update()
            return
        
        if verify_user(nome, senha):
            view_diets()
        else:
            warning_error()

    send_button = ft.ElevatedButton(text='Enviar', on_click=on_send_click)
    add_medic_button = ft.ElevatedButton(text='Cadastrar novo nutrólogo', on_click=add_medic)
    add_pacient_button = ft.ElevatedButton(text='Cadastrar novo paciente', on_click=add_pacient)
    
    page.add(name_field, password_field, send_button, add_medic_button, add_pacient_button, radio_group)

    def doctor_registration(e):
            global R, P, E
            nome = R.value.strip()
            senha = P.value.strip()
            email = E.value.strip()

            if not nome or not senha or not email:
                snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
                page.snack_bar = snack_bar
                snack_bar.open = True
                page.update()
                return

            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO usuario (nome, senha, email) VALUES (%s, %s, %s)",
                            (nome, senha, email)
                        )
                        conn.commit()
                        snack_bar = ft.SnackBar(ft.Text("Nutrólogo cadastrado com sucesso!"))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar nutrólogo."))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()
                page.update()

    def pacient_registration(e):
                nome = T.value.strip()
                senha = W.value.strip()
                email = S.value.strip()

                if not nome or not senha or not email:
                    snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    page.update()
                    return

                conn = create_connection()
                if conn:
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                "INSERT INTO usuario (nome, senha, email) VALUES (%s, %s, %s)",
                                (nome, senha, email)
                            )
                            conn.commit()
                            snack_bar = ft.SnackBar(ft.Text("Paciente cadastrado com sucesso!"))
                            page.snack_bar = snack_bar
                            snack_bar.open = True
                    except Error as e:
                        snack_bar = ft.SnackBar(ft.Text("Erro ao cadastrar paciente."))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                        print(f"Ocorreu um erro ao executar a consulta: {e}")
                    finally:
                        conn.close()
                    page.update()

def cadastrar_dieta(e):
    dialug = ft.AlertDialog(
            title=ft.Text("Cadastro de dieta"),
            actions=[ft.ElevatedButton(text='Cadastrar nova dieta', on_click='')],
            content=ft.Column([
                ft.Text("Nome da dieta"),
                ft.TextField(id='nome_dieta', hint_text='Nome da dieta'),
                ft.Text("Descrição da dieta"),
                ft.TextField(id='descricao_dieta', hint_text='Descrição da dieta'),
                ft.Text("Quantidade de calorias"),
                ft.TextField(id='calorias', hint_text='Quantidade de calorias'),
                ft.Text("Quantidade de proteínas"),
                ft.TextField(id='proteinas', hint_text='Quantidade de proteínas'),
                ft.Text("Quantidade de carboidratos"),
                ft.TextField(id='carboidratos', hint_text='Quantidade de carboidratos'),
                ft.Text("Quantidade de gorduras"),
                ft.TextField(id='gorduras', hint_text='Quantidade de gorduras'),
                ])
                )
    page = ft.Page(dialug)
    nome_dieta = page.root.find('nome_dieta').value
    descricao_dieta = page.root.find('descricao_dieta').value
    calorias = page.root.find('calorias').value
    proteínas = page.root.find('proteinas').value
    carboidratos = page.root.find('carboidratos').value
    gorduras = page.root.find('gorduras').value
    
    nome_dieta = ft.TextField(label="Nome da dieta", text_align=ft.TextAlign.LEFT)
    descricao_dieta = ft.TextField(label="Descrição da dieta", text_align=ft.TextAlign.LEFT)

    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO dieta (nome, descricao) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nome_dieta, descricao_dieta, calorias, proteínas, carboidratos, gorduras)
                )
                conn.commit()
                snack_bar = ft.SnackBar(ft.Text("Dieta cadastrada com sucesso!"))
                page.snack_bar = snack_bar
                snack_bar.open = True
        except Exception as e:
            snackbar = ft.SnackBar(ft.Text("Ocorreu um erro ao cadastrar a dieta."))
            page.snack_bar = snackbar
            snackbar.open = True
            print(f"Erro ao cadastrar dieta: {e}")
        finally:
            conn.close()

    page.overlay.append(dialug)
    dialug.open = True
    page.update()

def view_diets(page: ft.page):
    page.title = 'Lista de dietas'
    page.theme = ft.Theme(color_scheme_seed='red')
    page.background_color = ft.Color('white')
    page.padding = ft.Row([10, 10])
    page.content = ft.Column([
        ft.Text('Dietas'),
        ft.Button('Cadastrar dieta', on_click=cadastrar_dieta), #Concluir os defs
        ft.Button('Listar dietas', on_click=listar_dieta),
        ft.Button('Excluir dieta', on_click=excluir_dieta),
        ft.Button('Atualizar dieta', on_click=atualizar_dieta),
        ft.Button('Consultar dieta', on_click=consultar_dieta),
        ft.Button('Cadastrar paciente', on_click=pacient_registration),
        ])
    page.update()

    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM dieta")
                rows = cursor.fetchall()
                page.diets = rows
                page.update()
        except Error as e:
                print(f"Ocorreu um erro ao executar a consulta: {e}")
        finally:
            conn.close()

ft.app(target=menu)