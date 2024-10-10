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
    
    radios_group = ft.RadioGroup(
        value='Nutrólogo',
        content=ft.Column(
            controls=[
                ft.Radio(value="Nutrólogo", label="Nutrólogo"),
                ft.Radio(value='Paciente', label='Paciente')
            ]
        )
    )
    
    name_field = ft.TextField(label='Nome:', keyboard_type=ft.KeyboardType.TEXT, text_align=ft.TextAlign.LEFT)
    password_field = ft.TextField(label='Senha:', password=True, keyboard_type=ft.KeyboardType.NUMBER,text_align=ft.TextAlign.LEFT)

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
        
        if verify_user(nome, senha) and radios_group.value=='Nutrólogo':
            second_page(page)
        elif verify_user(nome, senha) and radios_group.value=='Paciente':
            third_page(page)
        else:
            warning_error()

    send_button = ft.ElevatedButton(text='Enviar', icon=ft.icons.SEND, on_click=on_send_click)
    add_medic_button = ft.ElevatedButton(text='Cadastrar novo nutrólogo', icon=ft.icons.ADD, on_click=add_medic)
    add_pacient_button = ft.ElevatedButton(text='Cadastrar novo paciente', icon=ft.icons.ADD,  on_click=add_pacient)
    
    page.add(name_field, password_field, send_button, add_medic_button, add_pacient_button, radios_group)

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
                        "INSERT INTO usuario (nome, senha, email, tipo) VALUES (%s, %s, %s, 'nutrólogo')",
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
        global T, W, S
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
                        "INSERT INTO usuario (nome, senha, email, tipo) VALUES (%s, %s, %s, 'paciente')",
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
        nome_field = ft.TextField(label="Nome da dieta:")
        calorias_field = ft.TextField(label="Calorias:", keyboard_type=ft.KeyboardType.NUMBER)
        proteinas_field = ft.TextField(label="Proteínas:", keyboard_type=ft.KeyboardType.NUMBER)
        carboidratos_field = ft.TextField(label="Carboidratos:", keyboard_type=ft.KeyboardType.NUMBER)
        gorduras_field = ft.TextField(label="Gorduras:", keyboard_type=ft.KeyboardType.NUMBER)

        dialogos = ft.AlertDialog(
            title=ft.Text("Cadastrar Dieta"),
            content=ft.Column([
                nome_field,
                calorias_field,
                proteinas_field,
                carboidratos_field,
                gorduras_field,
            ]),
            actions=[
                ft.ElevatedButton(
                    text='Cadastrar',
                    on_click=lambda e: save_dieta(
                        nome_field.value,
                        calorias_field.value,
                        proteinas_field.value,
                        carboidratos_field.value,
                        gorduras_field.value
                    )
                ),
            ]
        )
        page.overlay.append(dialogos)
        dialogos.open = True
        page.update()

    def save_dieta(nome, calorias, proteinas, carboidratos, gorduras):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO dieta (nome, calorias, proteinas, carboidratos, gorduras) VALUES (%s, %s, %s, %s, %s)",
                        (nome, calorias, proteinas, carboidratos, gorduras)
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
        page.update()

    def view_infos_paciente(page: ft.Page, nome_paciente: str):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT nome, email FROM usuario WHERE nome = %s", (nome_paciente,))
                    paciente = cursor.fetchone()
                    if paciente:
                        nome, email = paciente
                        info_text = f'Nome: {nome}\nEmail: {email}'
                    else:
                        info_text = "Paciente não encontrado."
            except Error as e:
                info_text = "Erro ao buscar informações do paciente."
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()
        else:
            info_text = "Erro na conexão com o banco de dados."

        page.controls.clear()
        page.title = 'Informações do Paciente'
        page.add(ft.Text(info_text, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK))
        page.add(ft.ElevatedButton(text='Voltar', on_click=lambda e: second_page(page)))
        page.update()

    def third_page(page: ft.Page):
        page.controls.clear()
        page.title = 'Menu do Paciente'
        page.dark_theme = ft.Theme(color_scheme_seed='red')
        page.padding = ft.Row([10, 10])

        nome_paciente = 'NomeDoPaciente'
        
        page.add(ft.Column([
            ft.FilledButton('Visualizar Informações do Paciente', on_click=lambda e: view_infos_paciente(page, nome_paciente)),
            ft.FilledButton('Listar dietas', on_click=listar_dieta),
            ft.FilledButton('Consultar dieta', on_click=consultar_dieta),
        ]))
        page.update()

    def listar_dieta(e):
        diet_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Calorias totais")),
            ]
        )
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM dieta")
                    rows = cursor.fetchall()
                    diet_table.rows.clear()
                    
                    for dieta in rows:
                        diet_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(dieta[1])),
                                ft.DataCell(ft.Text(dieta[2])),
                            ])
                        )
                table_container = ft.Container(
                    content=ft.Column(
                        controls=[diet_table],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=300,
                    border_radius=ft.border_radius.all(10),
                    padding=ft.padding.all(10),
                )
                page.controls.clear()
                page.add(table_container)
                page.update()
            except Exception as e:
                snack_bar = ft.SnackBar(ft.Text('Erro ao listar dietas.'))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()
            
            page.controls.clear()
            page.title = 'Listar Dietas'
            page.add(diet_table)
            ft.app(target=listar_dieta)

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
                            detail_text = f'Dieta: {dieta[1]}'
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
            ]),
        )
        
        detail_label = dialog.content[1]
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def second_page(page: ft.Page):
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
        ]))
        page.update()

ft.app(target=menu)