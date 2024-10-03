import flet as ft
import pymysql
from pymysql import Error

def create_connection():
    """Cria uma conexão com o banco de dados MySQL."""
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='acesso123',
            database='diets'
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
        P = ft.TextField(label='Digite sua senha:', password=True, keyboard_type=ft.KeyboardType.EMAIL)
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
        W = ft.TextField(label='Digite seu email:', keyboard_type=ft.KeyboardType.EMAIL)
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
            view_diets(page)
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

    def cadastrar_dieta(page: ft.Page):
        def save_dieta(nome, descricao, calorias, proteinas, carboidratos, gorduras):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO dieta (nome, descricao, calorias, proteinas, carboidratos, gorduras) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nome, descricao, calorias, proteinas, carboidratos, gorduras)
                        )
                        conn.commit()
                        snack_bar = ft.SnackBar(ft.Text(f'Dieta "{nome}" cadastrada com sucesso!'))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao cadastrar dieta.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        dialogos = ft.AlertDialog(
            title=ft.Text("Cadastrar Dieta"),
            content=ft.Column([
                ft.TextField(label="Nome da dieta:"),
                ft.TextField(label="Descrição:"),
                ft.TextField(label="Calorias:", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Proteínas:", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Carboidratos:", keyboard_type=ft.KeyboardType.NUMBER),
                ft.TextField(label="Gorduras:", keyboard_type=ft.KeyboardType.NUMBER),
            ]),
            actions=[
                ft.ElevatedButton(text='Cadastrar', on_click=lambda e: save_dieta(
                    dialogos.content[0].value,
                    dialogos.content[1].value,
                    dialogos.content[2].value,
                    dialogos.content[3].value,
                    dialogos.content[4].value,
                    dialogos.content[5].value
                )),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: dialogos.close()),
            ]
        )
        
        page.overlay.append(dialogos)
        dialogos.open = True
        page.update()
# view paciente
    def listar_dieta(page: ft.Page):
        def load_diets():
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT * FROM dieta")
                        rows = cursor.fetchall()

                        diet_list = ft.Column([ft.Text(f'Dieta: {dieta[1]} - Descrição: {dieta[2]}') for dieta in rows])
                        diet_container.controls.append(diet_list)
                        page.update()
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao listar dietas.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        page.controls.clear()
        page.title = 'Listar Dietas'
        diet_container = ft.Column()
        page.add(diet_container)

        load_diets()
        page.update()

    def excluir_dieta(page: ft.Page):
        def delete_dieta(nome_dieta):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM dieta WHERE nome = %s", (nome_dieta,))
                        conn.commit()
                        snack_bar = ft.SnackBar(ft.Text(f'Dieta "{nome_dieta}" excluída com sucesso!'))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao excluir dieta.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        dialog = ft.AlertDialog(
            title=ft.Text("Excluir Dieta"),
            content=ft.TextField(label="Nome da dieta a ser excluída:"),
            actions=[
                ft.ElevatedButton(text='Excluir', on_click=lambda e: delete_dieta(dialog.content.value)),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: dialog.close()),
            ]
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def atualizar_dieta(page: ft.Page):
        def update_dieta(nome_dieta, nova_descricao):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("UPDATE dieta SET descricao = %s WHERE nome = %s", (nova_descricao, nome_dieta))
                        conn.commit()
                        snack_bar = ft.SnackBar(ft.Text(f'Dieta "{nome_dieta}" atualizada com sucesso!'))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao atualizar dieta.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        dialog = ft.AlertDialog(
            title=ft.Text("Atualizar Dieta"),
            content=ft.Column([
                ft.TextField(label="Nome da dieta:"),
                ft.TextField(label="Nova descrição:"),
            ]),
            actions=[
                ft.ElevatedButton(text='Atualizar', on_click=lambda e: update_dieta(dialog.content[0].value, dialog.content[1].value)),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: dialog.close()),
            ]
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    def consultar_dieta(page: ft.Page):
        def search_dieta(nome_dieta):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT * FROM dieta WHERE nome = %s", (nome_dieta,))
                        dieta = cursor.fetchone()
                        if dieta:
                            detail_text = f'Dieta: {dieta[1]}\nDescrição: {dieta[2]}'
                        else:
                            detail_text = "Dieta não encontrada."
                        detail_label.value = detail_text
                        page.update()
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao consultar dieta.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        dialog = ft.AlertDialog(
            title=ft.Text("Consultar Dieta"),
            content=ft.Column([
                ft.TextField(label="Nome da dieta:", on_submit=lambda e: search_dieta(e.control.value)),
                ft.Text('', id='dieta_details'),
            ]),
            actions=[
                ft.ElevatedButton(text='Fechar', on_click=lambda e: dialog.close()),
            ]
        )
        
        detail_label = dialog.content[1]
        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    def view_diets(page: ft.Page):
        def load_diets():
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT * FROM dieta")
                        rows = cursor.fetchall()

                        diet_list = ft.Column([ft.Text(f'Dieta: {dieta[1]}') for dieta in rows])
                        diet_container.controls.append(diet_list)
                        page.update()
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Ocorreu um erro ao exibir as dietas.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        page.controls.clear()
        page.title = 'Lista de dietas'
        page.dark_theme = ft.Theme(color_scheme_seed='red')
        page.padding = ft.Row([10, 10])
        
        diet_container = ft.Column()
        page.add(diet_container)

        page.add(ft.Column([
            ft.FilledButton('Cadastrar dieta', on_click=cadastrar_dieta),
            ft.FilledButton('Listar dietas', on_click=listar_dieta),
            ft.FilledButton('Excluir dieta', on_click=excluir_dieta),
            ft.FilledButton('Atualizar dieta', on_click=atualizar_dieta),
            ft.FilledButton('Consultar dieta', on_click=consultar_dieta),
            ft.FilledButton('Cadastrar paciente', on_click=pacient_registration),
        ]))
        load_diets()
        page.update()

ft.app(target=menu)
