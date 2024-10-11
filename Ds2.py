import flet as ft
import pymysql
from pymysql import Error

def create_connection():
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='acesso123',
            database='diets'
        )
        return connection
    except Error as e:
        print(f"Ocorreu um erro: {e}")
        return None

def verify_user(nome, senha):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT tipo FROM usuario WHERE nome = %s AND senha = %s", (nome, senha))
                resultado = cursor.fetchone()
                if resultado:
                    print(f"Tipo de usuário encontrado: {resultado[0]}")
                    return resultado[0]
        except Error as e:
            print(f"Ocorreu um erro ao verificar usuário: {e}")
        finally:
            conn.close()
    return None

def menu(page: ft.Page):
    page.title = "Acompanhamento de dietas"
    page.theme = ft.Theme(color_scheme_seed='yellow')
    page.add(ft.Text(value='Bem vindo!', size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK))

    name_field = ft.TextField(label='Nome:', keyboard_type=ft.KeyboardType.TEXT, text_align=ft.TextAlign.LEFT)
    password_field = ft.TextField(label='Senha:', password=True, keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.LEFT)

    def add_user(e):
        tipo_user = ft.RadioGroup(
            value='nutrólogo',
            content=ft.Column(
                controls=[
                    ft.Radio(value="nutrólogo", label="Nutrólogo"),
                    ft.Radio(value='paciente', label='Paciente')
                ]
            )
        )
        
        R = ft.TextField(label="Digite seu nome:", text_align=ft.TextAlign.LEFT)
        P = ft.TextField(label='Digite sua senha:', password=True, keyboard_type=ft.KeyboardType.NUMBER)
        E = ft.TextField(label='Digite seu email:', text_align=ft.TextAlign.LEFT)

        dialog = ft.AlertDialog(
            title=ft.Text("Cadastro de Usuário"),
            content=ft.Column([R, P, E, tipo_user]),
            actions=[ft.ElevatedButton(text='Cadastrar', on_click=lambda e: user_registration(R.value, P.value, E.value, tipo_user.value))],
        )

        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def user_registration(nome, senha, email, tipo):
        if not nome or not senha or not email or not tipo:
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
                        "INSERT INTO usuario (nome, senha, email, tipo) VALUES (%s, %s, %s, %s)",
                        (nome, senha, email, tipo)
                    )
                    conn.commit()
                    snack_bar = ft.SnackBar(ft.Text(f"{tipo.capitalize()} cadastrado com sucesso!"))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
            except Error as e:
                snack_bar = ft.SnackBar(ft.Text(f"Erro ao cadastrar {tipo}."))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()
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

        usuario_tipo = verify_user(nome, senha)
        print(f"Usuário: {nome}, Tipo de usuário: {usuario_tipo}")

        if usuario_tipo and usuario_tipo.lower() == "nutrólogo":
            second_page(page)
        elif usuario_tipo and usuario_tipo.lower() == "paciente":
            third_page(page)
        else:
            warning_error()

    send_button = ft.ElevatedButton(text='Enviar', icon=ft.icons.SEND, on_click=on_send_click)
    add_user_button = ft.ElevatedButton(text='Cadastrar novo usuário', icon=ft.icons.ADD, on_click=add_user)
    
    page.add(name_field, password_field, send_button, add_user_button)

    def cadastrar_dieta(e):
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

    def third_page(page: ft.Page):
            page.controls.clear()
            page.title = 'Menu do Paciente'
            page.dark_theme = ft.Theme(color_scheme_seed='red')
            page.padding = ft.Row([10, 10])
            
            page.add(ft.Column([
                ft.FilledButton('Listar dietas', on_click=listar_dieta),
                ft.FilledButton('Pesquisar dieta', on_click=pesquisar_dieta),
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
                    height=400,
                    border_radius=ft.border_radius.all(10),
                    padding=ft.padding.all(10),
                )
                back_button = ft.ElevatedButton(
                    text="Voltar",
                    on_click=lambda e: second_page(page)
                )
                main_column = ft.Column(
                    controls=[
                        ft.Text("Lista de dietas", size=24, weight="bold"),
                        table_container,
                        back_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
                page.controls.clear()
                page.add(main_column)
                page.update()
            
            except Exception as e:
                snack_bar = ft.SnackBar(ft.Text('Erro ao listar dietas.'))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            
            finally:
                conn.close()

    def listar_alimentos(e):
        food_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome do Alimento")),
                ft.DataColumn(ft.Text("Calorias")),
            ]
        )
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM alimento")
                    rows = cursor.fetchall()
                    food_table.rows.clear()
                    
                    for alimento in rows:
                        food_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(alimento[1])),
                                ft.DataCell(ft.Text(alimento[2])),
                            ])
                        )
                table_container = ft.Container(
                    content=ft.Column(
                        controls=[food_table],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=400,
                    border_radius=ft.border_radius.all(10),
                    padding=ft.padding.all(10),
                )
                back_button = ft.ElevatedButton(
                    text="Voltar",
                    on_click=lambda e: second_page(page)
                )
                main_column = ft.Column(
                    controls=[
                        ft.Text("Lista de Alimentos", size=24, weight="bold"),
                        table_container,
                        back_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
                page.controls.clear()
                page.add(main_column)
                page.update()
            
            except Exception as e:
                snack_bar = ft.SnackBar(ft.Text('Erro ao listar alimentos.'))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            
            finally:
                conn.close()

    def save_alimento(nome, quantidade, unidade, calorias, proteinas, gorduras, carboidratos):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO alimento (nome, quantidade, unidade, proteínas, carboidratos, gorduras, calorias) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (nome, quantidade, unidade, proteinas, carboidratos, gorduras, calorias)
                    )
                    conn.commit()
                    snack_bar = ft.SnackBar(ft.Text('Alimento salvo com sucesso.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    page.controls.clear()
            except Error as e:
                snackbar = ft.SnackBar(ft.Text("Ocorreu um erro ao cadastrar o alimento, tente novamente."))
                page.snack_bar = snackbar
                snackbar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()

    def save_alimentos(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Salvar Alimento"),
            content=ft.Column(
                [
                    ft.TextField(label='Nome do alimento:'),
                    ft.TextField(label='Quantidade do alimento:'),
                    ft.TextField(label='Unidade do alimento: Gramas, Kg ou Mililitros(ml)'),
                    ft.TextField(label='Calorias:'),
                    ft.TextField(label='Proteínas:'),
                    ft.TextField(label='Gorduras:'),
                    ft.TextField(label='Carboidratos:')
                ]
            ),
            actions=[
                ft.TextButton('Salvar', on_click=lambda e: save_alimento(
                    dialog.content.controls[0].value,
                    dialog.content.controls[1].value,
                    dialog.content.controls[2].value,
                    dialog.content.controls[3].value,
                    dialog.content.controls[4].value,
                    dialog.content.controls[5].value,
                    dialog.content.controls[6].value
                )),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    def excluir_dieta(e):
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
                    snackbar = ft.SnackBar(ft.Text('Erro ao excluir dieta.'))
                    page.snack_bar = snackbar
                    snackbar.open = True
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

    def atualizar_dieta(e):             #Este def precisa ser atualizado mais para a frente
        def update_dieta(nome_dieta):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("UPDATE dieta SET = %s WHERE nome = %s", (nome_dieta))
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
            ]),
            actions=[
                ft.ElevatedButton(text='Atualizar', on_click=lambda e: update_dieta(dialog.content[0].value, dialog.content[1].value)),
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def pesquisar_dieta(e):
        def search_dieta(nome_dieta):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT * FROM dieta WHERE nome = %s", (nome_dieta,))
                        dieta = cursor.fetchone()
                        if dieta:
                            data_table.rows = [
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text(dieta[0])),
                                    ft.DataCell(ft.Text(dieta[1])),
                                    ft.DataCell(ft.Text(dieta[2])),
                                ])
                            ]
                        else:
                            data_table.rows = [
                                ft.DataRow(cells=[ft.DataCell(ft.Text("Dieta não encontrada."))])
                            ]
                        page.update()
                except Error as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao consultar dieta.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Quantidade de calorias")),
        ]
        data_table = ft.DataTable(columns=columns, rows=[])

        dialog = ft.AlertDialog(
            title=ft.Text("Pesquisar Dieta"),
            content=ft.Column([
                ft.TextField(label="Nome da dieta:", on_submit=lambda e: search_dieta(e.control.value)),
                data_table,
            ]),
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def second_page(page: ft.Page):
        page.controls.clear()
        page.title = 'Menu do Nutrólogo'
        
        page.add(ft.Column([
            ft.Text(f'Bem-vindo!', size=20),
            ft.FilledButton('Cadastrar dieta', on_click=cadastrar_dieta),
            ft.FilledButton('Listar dietas', on_click=listar_dieta),
            ft.FilledButton('Excluir dieta', on_click=excluir_dieta),
            ft.FilledButton('Atualizar dieta', on_click=atualizar_dieta),
            ft.FilledButton('Pesquisar dieta', on_click=pesquisar_dieta),
            ft.FilledButton('Cadastrar alimentos',on_click=save_alimentos),
            ft.FilledButton('Listar alimentos',on_click=listar_alimentos),
        ]))
        page.update()

ft.app(target=menu)
