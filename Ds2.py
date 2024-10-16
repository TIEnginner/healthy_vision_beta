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
    page.title = "Healthy Vision"
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

        dieta_dropdown = ft.Dropdown(label="Selecione a dieta:", options=[])

        dialog = ft.AlertDialog(
            title=ft.Text("Cadastro de Usuário"),
            content=ft.Column([R, P, E, tipo_user, dieta_dropdown]),
            actions=[ft.ElevatedButton(
                text='Cadastrar',
                on_click=lambda e: user_registration(R.value, P.value, E.value, tipo_user.value, dieta_dropdown.value)
            )],
        )
        load_dietas(dieta_dropdown)
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def load_dietas(dropdown):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT nome FROM dieta")
                    dietas = cursor.fetchall()
                    dropdown.options.clear()  # Limpa as opções existentes.
                    
                    if not dietas:
                        print("Nenhuma dieta encontrada na tabela 'dieta'.")
                    else:
                        for dieta in dietas:
                            nome_dieta = dieta[0].strip()  # Remove espaços em branco
                            dropdown.options.append(ft.Dropdown(label=nome_dieta, value=nome_dieta))  # Adiciona dietas ao dropdown.
                        print(f"Dietas carregadas: {[dieta[0] for dieta in dietas]}")  # Log das dietas carregadas.

            except Exception as e:
                print(f"Ocorreu um erro ao carregar as dietas: {e}")
            finally:
                conn.close()

    def user_registration(nome, senha, email, tipo, dieta):
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
                        "INSERT INTO usuario (nome, senha, email, tipo) VALUES (%s, %s, %s, %s);",
                        (nome, senha, email, tipo)
                    )
                    usuario_id = cursor.lastrowid

                    if dieta:
                        cursor.execute("SELECT id FROM dieta WHERE nome = %s", (dieta,))
                        dieta_id = cursor.fetchone()

                        if dieta_id:
                            dieta_id = dieta_id[0]
                            cursor.execute(
                                "UPDATE usuario SET id_dieta = %s WHERE id = %s",
                                (dieta_id, usuario_id)
                            )
                        else:
                            snack_bar = ft.SnackBar(ft.Text(f"Dieta '{dieta}' não encontrada."))
                            page.snack_bar = snack_bar
                            snack_bar.open = True
                            return

                    conn.commit()
                    snack_bar = ft.SnackBar(ft.Text(f"{tipo.capitalize()} cadastrado com sucesso!"))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
            except Exception as e:
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
        paciente_id_field = ft.TextField(label="ID do Paciente:", keyboard_type=ft.KeyboardType.NUMBER)

        dialogos = ft.AlertDialog(
            title=ft.Text("Cadastrar Dieta"),
            content=ft.Column([
                nome_field,
                calorias_field,
                proteinas_field,
                carboidratos_field,
                gorduras_field,
                paciente_id_field
            ]),
            actions=[
                ft.ElevatedButton(
                    text='Cadastrar',
                    on_click=lambda e: save_dieta(
                        nome_field.value,
                        calorias_field.value,
                        proteinas_field.value,
                        carboidratos_field.value,
                        gorduras_field.value,
                        paciente_id_field.value
                    )
                ),
            ]
        )
        page.overlay.append(dialogos)
        dialogos.open = True
        page.update()

    def save_dieta(nome, calorias, proteinas, carboidratos, gorduras, paciente_id):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO dieta (nome, calorias, proteinas, carboidratos, gorduras) VALUES (%s, %s, %s, %s, %s);",
                        (nome, calorias, proteinas, carboidratos, gorduras)
                    )
                    # Obtenha o último ID inserido
                    dieta_id = cursor.lastrowid
                    # Aqui atualiza o ID da dieta no usuário
                    cursor.execute(
                        "UPDATE usuario SET id_dieta = %s WHERE id = %s AND tipo = 'Paciente'",
                        (dieta_id, paciente_id)
                    )
                    conn.commit()  # Aqui a dieta é atribuída a um paciente.

                    snack_bar = ft.SnackBar(ft.Text(f'Dieta "{nome}" cadastrada e atribuída ao paciente com ID {paciente_id} com sucesso!'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
            except Exception as e:
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
                ft.FilledButton('Listar dietas', on_click=listar_dieta2, icon=ft.icons.LIST),
                ft.FilledButton('Pesquisar dieta', on_click=pesquisar_dieta, icon=ft.icons.SEARCH),
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

    def listar_dieta2(e):
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
                    on_click=lambda e: third_page(page)
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

    def excluir_alimento(e):
        def delete_alimento(nome_alimento):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM alimento WHERE nome = %s", (nome_alimento,))
                        conn.commit()
                        snack_bar = ft.SnackBar(ft.Text(f'Alimento "{nome_alimento}" excluído com sucesso!'))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                except Exception as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao excluir alimento.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        dialog = ft.AlertDialog(
            title=ft.Text("Excluir Alimento"),
            content=ft.TextField(label="Nome do alimento a ser excluído:"),
            actions=[
                ft.ElevatedButton(text='Excluir', on_click=lambda e: delete_alimento(dialog.content.value)),
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def editar_alimento(e):
        def update_alimento(nome_alimento, novo_nome, nova_caloria):
            conn = create_connection()
            if conn:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            UPDATE alimento 
                            SET nome = %s, calorias = %s 
                            WHERE nome = %s
                        """, (novo_nome, nova_caloria, nome_alimento))
                        conn.commit()
                        snack_bar = ft.SnackBar(ft.Text(f'Alimento "{nome_alimento}" editado com sucesso!'))
                        page.snack_bar = snack_bar
                        snack_bar.open = True
                except Exception as e:
                    snack_bar = ft.SnackBar(ft.Text('Erro ao editar alimento.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    print(f"Ocorreu um erro ao executar a consulta: {e}")
                finally:
                    conn.close()

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Alimento"),
            content=ft.Column([
                ft.TextField(label="Nome do alimento a ser editado:"),
                ft.TextField(label="Novo nome do alimento:"),
                ft.TextField(label="Nova quantidade de calorias:", keyboard_type=ft.KeyboardType.NUMBER)
            ]),
            actions=[
                ft.ElevatedButton(
                    text='Editar',
                    on_click=lambda e: update_alimento(
                        dialog.content.controls[0].value,
                        dialog.content.controls[1].value,
                        dialog.content.controls[2].value
                    )
                ),
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def pesquisar_alimento(e):
            def search_alimento(nome_alimento):
                conn = create_connection()
                if conn:
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute("SELECT * FROM alimento WHERE nome = %s", (nome_alimento,))
                            alimentos = cursor.fetchone()
                            if alimentos:
                                data_table.rows = [
                                    ft.DataRow(cells=[
                                        ft.DataCell(ft.Text(alimentos[0])),
                                        ft.DataCell(ft.Text(alimentos[1])),
                                        ft.DataCell(ft.Text(alimentos[2])),
                                    ])
                                ]
                            else:
                                data_table.rows = [
                                    ft.DataRow(cells=[ft.DataCell(ft.Text("Alimento não encontrado."))])
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
                title=ft.Text("Pesquisar Alimento"),
                content=ft.Column([
                    ft.TextField(label="Nome do alimento:", on_submit=lambda e: search_alimento(e.control.value)),
                    data_table,
                ]),
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    def save_refeicao(nome, horario, calorias, proteinas, gorduras, carboidratos):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO refeicao (nome, horario, calorias, proteinas, gorduras, carboidratos) VALUES (%s, %s, %s, %s, %s, %s)",
                        (nome, horario, calorias, proteinas, gorduras, carboidratos)
                    )
                    conn.commit()
                    snack_bar = ft.SnackBar(ft.Text('Refeição salva com sucesso.'))
                    page.snack_bar = snack_bar
                    snack_bar.open = True
                    page.controls.clear()
            except Error as e:
                snackbar = ft.SnackBar(ft.Text("Ocorreu um erro ao cadastrar a refeição, tente novamente."))
                page.snack_bar = snackbar
                snackbar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()

    def save_refeicoes(e):
        dialog = ft.AlertDialog(
            title=ft.Text("Salvar Refeição"),
            content=ft.Column(
                [
                    ft.TextField(label='Nome da refeição:'),
                    ft.TextField(label='Horário da refeição:'),
                    ft.TextField(label='Calorias:'),
                    ft.TextField(label='Proteínas:'),
                    ft.TextField(label='Gorduras:'),
                    ft.TextField(label='Carboidratos:')
                ]
            ),
            actions=[
                ft.TextButton('Salvar', on_click=lambda e: save_refeicao(
                    dialog.content.controls[0].value,
                    dialog.content.controls[1].value,
                    dialog.content.controls[2].value,
                    dialog.content.controls[3].value,
                    dialog.content.controls[4].value,
                    dialog.content.controls[5].value
                )),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def listar_refeicoes(e):
        refeicao_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome da Refeição")),
                ft.DataColumn(ft.Text("Horário")),
            ]
        )
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nome, horario FROM refeicao")
                    rows = cursor.fetchall()
                    refeicao_table.rows.clear()
                    
                    for refeicao in rows:
                        refeicao_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(refeicao[0])),  # ID da refeição
                                ft.DataCell(ft.Text(refeicao[1])),  # Nome da refeição
                                ft.DataCell(ft.Text(refeicao[2])),  # Horário da refeição
                            ])
                        )
                    table_container = ft.Container(
                        content=ft.Column(
                            controls=[refeicao_table],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        height=400,
                        border_radius=ft.border_radius.all(10),
                        padding=ft.padding.all(10),
                    )
                    back_button = ft.ElevatedButton(
                        text="Voltar",
                        on_click=lambda e: second_page(page)  # Ou a página que você deseja retornar
                    )
                    main_column = ft.Column(
                        controls=[
                            ft.Text("Lista de Refeições", size=24, weight="bold"),
                            table_container,
                            back_button,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    )
                    page.controls.clear()
                    page.add(main_column)
                    page.update()
                    
            except Error as e:
                snackbar = ft.SnackBar(ft.Text("Ocorreu um erro ao listar as refeições."))
                page.snack_bar = snackbar
                snackbar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()

    def excluir_refeicao(refeicao_id):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM refeicao WHERE id = %s", (refeicao_id,))
                    conn.commit()
                    snackbar = ft.SnackBar(ft.Text("Refeição excluída com sucesso."))
                    page.snack_bar = snackbar
                    snackbar.open = True
            except Error as e:
                snackbar = ft.SnackBar(ft.Text("Ocorreu um erro ao excluir a refeição."))
                page.snack_bar = snackbar
                snackbar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()

    def confirmar_exclusao(refeicao_id):
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir esta refeição?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.TextButton("Excluir", on_click=lambda e: [excluir_refeicao(refeicao_id), dialog.close()]),
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True

    def atualizar_refeicao(refeicao_id, nome_atual, horario_atual):
        dialog = ft.AlertDialog(
            title=ft.Text("Atualizar Refeição"),
            content=ft.Column(
                [
                    ft.TextField(label='Nome da refeição:', value=nome_atual),
                    ft.TextField(label='Horário da refeição:', value=horario_atual),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.close()),
                ft.TextButton("Atualizar", on_click=lambda e: [
                    salvar_atualizacao(refeicao_id, dialog.content.controls[0].value, dialog.content.controls[1].value),
                    dialog.close()
                ]),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True

    def salvar_atualizacao(refeicao_id, novo_nome, novo_horario):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE refeicao SET nome = %s, horario = %s WHERE id = %s",
                        (novo_nome, novo_horario, refeicao_id)
                    )
                    conn.commit()
                    snackbar = ft.SnackBar(ft.Text("Refeição atualizada com sucesso."))
                    page.snack_bar = snackbar
                    snackbar.open = True
            except Error as e:
                snackbar = ft.SnackBar(ft.Text("Ocorreu um erro ao atualizar a refeição."))
                page.snack_bar = snackbar
                snackbar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            finally:
                conn.close()

    def list_pacients(e):
        patient_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome do Paciente")),
                ft.DataColumn(ft.Text("Id")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Dieta Atribuída")),
            ]
        )
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT u.nome, u.id, u.email, d.nome 
                        FROM usuario u 
                        LEFT JOIN dieta d ON u.id_dieta = d.id 
                        WHERE u.tipo = 'Paciente'
                    """)
                    rows = cursor.fetchall()
                    patient_table.rows.clear()
                    
                    for paciente in rows:
                        patient_table.rows.append(
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(paciente[0])),  # Nome do paciente
                                ft.DataCell(ft.Text(paciente[1])),  # Id do paciente
                                ft.DataCell(ft.Text(paciente[2])),  # Email do paciente
                                ft.DataCell(ft.Text(paciente[3] if paciente[3] else "Nenhuma")),  # Dieta atribuída
                            ])
                        )
                
                table_container = ft.Container(
                    content=ft.Column(
                        controls=[patient_table],
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
                        ft.Text("Lista de Pacientes", size=24, weight="bold"),
                        table_container,
                        back_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
                page.controls.clear()
                page.add(main_column)
                page.update()
            
            except Exception as e:
                snack_bar = ft.SnackBar(ft.Text('Erro ao listar pacientes.'))
                page.snack_bar = snack_bar
                snack_bar.open = True
                print(f"Ocorreu um erro ao executar a consulta: {e}")
            
            finally:
                conn.close()

    def second_page(page: ft.Page):
        page.controls.clear()
        page.title = 'Menu do Nutrólogo'
        page.add(ft.Column([
            ft.Text(f'Bem-vindo!', size=20),
            ft.FilledButton('Cadastrar dieta', on_click=cadastrar_dieta, icon=ft.icons.ADD),
            ft.FilledButton('Listar dietas', on_click=listar_dieta, icon=ft.icons.LIST),
            ft.FilledButton('Excluir dieta', on_click=excluir_dieta, icon=ft.icons.DELETE),
            ft.FilledButton('Atualizar dieta', on_click=atualizar_dieta, icon=ft.icons.EDIT),       # Esta função precisa ser atualizada.
            ft.FilledButton('Pesquisar dieta', on_click=pesquisar_dieta, icon=ft.icons.SEARCH),
            ft.FilledButton('Listar pacientes',on_click=list_pacients, icon=ft.icons.LIST),
            ft.FilledButton('Cadastrar alimentos',on_click=save_alimentos, icon=ft.icons.ADD),
            ft.FilledButton('Listar alimentos',on_click=listar_alimentos, icon=ft.icons.LIST),
            ft.FilledButton('Excluir alimentos',on_click=excluir_alimento, icon=ft.icons.DELETE),
            ft.FilledButton('Atualizar alimentos',on_click=editar_alimento, icon=ft.icons.EDIT),
            ft.FilledButton('Pesquisar alimentos',on_click=pesquisar_alimento, icon=ft.icons.SEARCH),
            ft.FilledButton('Cadastrar refeições',on_click=save_refeicoes, icon=ft.icons.ADD),
            ft.FilledButton('Listar refeições',on_click=listar_refeicoes, icon=ft.icons.LIST),
            ft.FilledButton('Excluir refeições',on_click=excluir_refeicao, icon=ft.icons.DELETE),
            ft.FilledButton('Atualizar refeições',on_click=atualizar_refeicao, icon=ft.icons.EDIT),

        ]))
        page.update()

ft.app(target=menu)
