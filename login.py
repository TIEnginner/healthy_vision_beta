import flet as ft
import mysql.connector
import time

def main(page: ft.Page):
    global nome, senha, frame_cadastro

    def show_popup_login_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Login Sucesso"),
            content=ft.Text("Login realizado com sucesso!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def on_send_click(e, radio_group, nome_cadastro, senha_cadastro, repetir_senha, email_cadastro):
        if radio_group.value == 'Nutrólogo':
            nut = "nutrólogo"
            pac = None
        elif radio_group.value == 'Paciente':
            pac = "Paciente"
            nut = None

        salvar_cadastro(e, nome_cadastro, senha_cadastro, repetir_senha, email_cadastro, nut, pac)

    def salvar_cadastro(e, nome_cadastro, senha_cadastro, repetir_senha, email_cadastro, nut, pac):
        if senha_cadastro.value == repetir_senha.value:
            usuario = {
                "nome": nome_cadastro.value,
                "senha": senha_cadastro.value,
                "email": email_cadastro.value,
                "tipo": nut or pac
            }

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO usuario (nome, senha, email, tipo) VALUES (%s, %s, %s, %s)", 
                    (usuario["nome"], usuario["senha"], usuario["email"], usuario["tipo"])
                )
                conn.commit()

                show_popup_cadastro_sucesso()
                page.update()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()
            finally:
                cursor.close()
                conn.close()
        else:
            show_popup_cadastro_erro()

    def show_popup_cadastro_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text("Cadastro realizado com sucesso!"),
            actions=[ft.TextButton("OK", on_click=lambda e: (fechar_popup(), voltar_para_login()))],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def fechar_popup():
            popup.open = False
            page.update()
        
        page.dialog = popup
        popup.open = True
        page.update()

    def show_popup_cadastro_erro():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("As senhas não coincidem!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def senha_existe():
        popup = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text("Já existe um usuário com essa senha, tente outra senha!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def delete_frames():
        page.controls.clear()
        page.update()

    def show_popups(e):
        print("Tentando fazer login...")
        print(f"Nome: {nome.value}, Senha: {senha.value}")

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE nome = %s AND senha = %s", (nome.value, senha.value))

            result = cursor.fetchall()
            print(f"Resultado da consulta: {result}")

            if result:
                show_popup_login_sucesso()

                time.sleep(2)
                page_nutro(page)
            else:
                show_popup_usuario_nao_encontrado()

            time.sleep(2)

        except mysql.connector.Error as err:
            print(f"Erro ao verificar usuário: {err}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


    def show_popup_login_sucesso():
        popup = ft.AlertDialog(
            title=ft.Text("Login Sucesso"),
            content=ft.Text("Login realizado com sucesso!"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def show_popup_ahoba():
        popup = ft.AlertDialog(
            title=ft.Text("Erro!"),
            content=ft.Text("O email deve conter o @gmail.com/outlook para acessar a plataforma"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def show_popup_vasio():
        popup = ft.AlertDialog(
            title=ft.Text("Erro!"),
            content=ft.Text("Todos os campos devem ser preenchidos"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()

        page.dialog = popup
        popup.open = True
        page.update()

    def voltar_para_login():
        delete_frames()
        page.add(main_container)
        page.update()

    def verificar_email(email_cadastro, v_senha_existe, e):
        
        if "@" in email_cadastro.value and len(email_cadastro.value.split('@')[0]) > 0:
            dominio = email_cadastro.value.split('@')[1]
            if dominio in ["gmail.com", "outlook.com"]:
                v_senha_existe(e)
            else:
                show_popup_ahoba()
        else:
            show_popup_ahoba()

    def verificar_campos(e, label_cadastro, nome_cadastro, email_cadastro, senha_cadastro, repetir_senha, v_senha_existe):

        if any(not field.value for field in [nome_cadastro, email_cadastro, senha_cadastro, repetir_senha]):
            show_popup_vasio()
        else:
            verificar_email(email_cadastro, v_senha_existe, e)

    def abrir_cadastro():
        page.controls.clear()

        label_cadastro = ft.Text("Cadastro", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        nome_cadastro = ft.TextField(label="Nome")
        email_cadastro = ft.TextField(label="Email")
        senha_cadastro = ft.TextField(label="Senha", password=True)
        repetir_senha = ft.TextField(label="Repetir Senha", password=True)

        def v_senha_existe(e):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT senha FROM usuario")
                result = cursor.fetchall()

                for resultado in result:
                    if resultado[0] == senha_cadastro.value:
                        senha_existe()
                        return

                on_send_click(e, radio_group, nome_cadastro, senha_cadastro, repetir_senha, email_cadastro)

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()
            finally:
                cursor.close()
                conn.close()

        radio_group = ft.RadioGroup(
            value='Paciente',
            content=ft.Column(
                controls=[
                    ft.Radio(value="Nutrólogo", label="Nutrólogo"),
                    ft.Radio(value='Paciente', label='Paciente')
                ]
            )
        )

        botao_cadastrar = ft.ElevatedButton(
            text="Cadastrar",
            on_click=lambda e: verificar_campos(e, label_cadastro, nome_cadastro, email_cadastro, senha_cadastro, repetir_senha, v_senha_existe)
        )
    
        frame_cadastro = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(label_cadastro, alignment=ft.alignment.center, bgcolor="#4D4D4D", padding=18),
                    ft.Container(nome_cadastro, alignment=ft.alignment.center),
                    ft.Container(senha_cadastro, alignment=ft.alignment.center),
                    ft.Container(repetir_senha, alignment=ft.alignment.center),
                    ft.Container(email_cadastro, alignment=ft.alignment.center),
                    ft.Container(botao_cadastrar, alignment=ft.alignment.center),
                    ft.Container(radio_group, alignment=ft.alignment.center),
                ]
            ),
            bgcolor="#696969",
            width=400,
            height=480,
            border_radius=10,
            alignment=ft.alignment.center,
            padding=20
        )

        frame_container = ft.Container(
            content=frame_cadastro,
            alignment=ft.alignment.center,
            padding=115
        )

        main_container = ft.Column(
            controls=[frame_container],
            alignment=ft.MainAxisAlignment.START,
        )

        page.add(main_container)
        page.update()

    page.title = "Supermercado"
    page.window.full_screen = False  # Muda para False para não ser tela cheia
    page.window.width = 1250  # Defina uma largura adequada para sua aplicação
    page.window.height = 800  # Defina uma altura adequada para sua aplicação

    label = ft.Text("Biblioteca Acervo", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
    label1 = ft.Text("Login")
    label2 = ft.Text("Nome")
    label3 = ft.Text("Senha")
    label4 = ft.Text("Não tem uma conta?")

    nome = ft.TextField(label="Nome")
    senha = ft.TextField(label="Senha", password=True)

    def handle_login_click(e):
        show_popups(e)


    botao = ft.ElevatedButton(text="X", on_click=lambda e: page.window.destroy())
    botao1 = ft.ElevatedButton(text="Entrar", on_click= handle_login_click)
    botao2 = ft.ElevatedButton(text="Cadastrar", on_click=lambda e: abrir_cadastro())

    frame = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(label, alignment=ft.alignment.center, bgcolor="#4D4D4D"),
                ft.Container(label1, alignment=ft.alignment.center),
                ft.Container(label2, alignment=ft.alignment.center),
                ft.Container(nome, alignment=ft.alignment.center),
                ft.Container(label3, alignment=ft.alignment.center),
                ft.Container(senha, alignment=ft.alignment.center),
                ft.Container(botao1, alignment=ft.alignment.center),
                ft.Container(label4, alignment=ft.alignment.center),
                ft.Container(botao2, alignment=ft.alignment.center),
            ]
        ),
        bgcolor="#696969",
        width=400,
        height=500,
        border_radius=10,
        alignment=ft.alignment.center,
        padding=20
    )

    def show_popup_usuario_nao_encontrado():
        popup = ft.AlertDialog(
            title=ft.Text("Usuário Não Encontrado"),
            content=ft.Text("O usuário não foi encontrado. Deseja se cadastrar?"),
            actions=[
                ft.TextButton("Cadastrar", on_click=lambda e: (setattr(popup, "open", False), abrir_cadastro())),
                ft.TextButton("Cancelar", on_click=lambda e: fechar_popup())
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()
            
        page.dialog = popup
        popup.open = True
        page.update()

    frame_container = ft.Container(
        content=frame,
        alignment=ft.alignment.center,
        padding=20
    )

    button_container = ft.Container(
        content=botao,
        alignment=ft.alignment.top_right,
        padding=20
    )

    main_container = ft.Column(
        controls=[
            button_container,
            frame_container
        ],
        alignment=ft.MainAxisAlignment.START,
    )

    page.add(main_container)
    page.update()

    def build_custom_navbar(page, page_dietas):
        def handle_nav_click(label):
            if label == "Gerenciar dietas":
                page_dietas()
            elif label == "Alimentos":
                print("Botão 'Alimentos' clicado")
                # Adicione a lógica para "Alimentos" aqui
            elif label == "Configurações":
                print("Botão 'Configurações' clicado")
                # Adicione a lógica para "Configurações" aqui

        # Itens da barra lateral
        nav_items = [
            {"label": "Gerenciar dietas", "icon": ft.icons.FOOD_BANK_OUTLINED},
            {"label": "Alimentos", "icon": ft.icons.KITCHEN},
            {"label": "Configurações", "icon": ft.icons.SETTINGS},
        ]

        # Simulação da barra lateral com botões
        sidebar_content = ft.Column(
            [
                ft.Text("Workspace", size=20, color=ft.colors.WHITE),
                ft.Container(
                    bgcolor=ft.colors.BLACK26,
                    height=1,
                    width=200,
                ),
                *[
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(nav_item["icon"], size=25, color=ft.colors.WHITE),
                                ft.Text(nav_item["label"], size=18, color=ft.colors.WHITE)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=10
                        ),
                        padding=ft.padding.symmetric(vertical=10),
                        bgcolor="#4F4F4F",
                        border_radius=ft.border_radius.all(5),
                        height=40,
                        on_click=lambda e, lbl=nav_item["label"]: handle_nav_click(lbl),  # Aqui passamos o rótulo correto
                    )
                    for nav_item in nav_items
                ],
                ft.Container(
                    bgcolor=ft.colors.BLACK26,
                    height=1,
                    width=200,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )

        # Container da barra lateral
        sidebar_frame = ft.Container(
            content=sidebar_content,
            width=250,
            height=page.window_height,
            bgcolor="#4F4F4F",
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(10)
        )

        return sidebar_frame
    def deletar_dieta(page: ft.Page):
        nome_field = ft.TextField(label="Nome da dieta a ser deletada:")

        dialogo_deletar = ft.AlertDialog(
            title=ft.Text("Deletar Dieta"),
            content=ft.Column([
                nome_field,
            ]),
            actions=[
                ft.ElevatedButton(
                    text='Deletar',
                    on_click=lambda e: remover_dieta(nome_field.value, dialogo_deletar, page)
                ),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: page.overlay.remove(dialogo_deletar)),
            ]
        )

        page.overlay.append(dialogo_deletar)
        dialogo_deletar.open = True
        page.update()

    def remover_dieta(nome, dialogo_deletar, page):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT nome FROM dieta WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                cursor.execute("DELETE FROM dieta WHERE nome = %s", (nome,))
                conn.commit()

                popup_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text("Dieta deletada com sucesso!"),
                    actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_sucesso))]
                )
                page.overlay.append(popup_sucesso)
                popup_sucesso.open = True
                page.overlay.remove(dialogo_deletar)

            else:
                popup_erro = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text("Dieta não encontrada."),
                    actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_erro))]
                )
                page.overlay.append(popup_erro)
                popup_erro.open = True

        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        finally:
            cursor.close()
            conn.close()

        page.update()

    def cadastrar_dieta(page: ft.Page):
        nome_field = ft.TextField(label="Nome da dieta:")
        calorias_field = ft.TextField(label="Calorias Totais:", keyboard_type=ft.KeyboardType.NUMBER)

        dialogos = ft.AlertDialog(
            title=ft.Text("Cadastrar Dieta"),
            content=ft.Column([
                nome_field,
                calorias_field,
            ]),
            actions=[
                ft.ElevatedButton(
                    text='Cadastrar',
                    on_click=lambda e: inserir_dieta(nome_field.value, calorias_field.value, dialogos, page)
                ),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: page.overlay.remove(dialogos)),
            ]
        )

        page.overlay.append(dialogos)
        dialogos.open = True
        page.update()

    def inserir_dieta(nome, calorias, dialogos, page):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT nome FROM dieta WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                popup_erro = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text("Essa dieta já existe."),
                    actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_erro))]
                )

                page.update()
                page.overlay.append(popup_erro)
                popup_erro.open = True
            else:
                query = "INSERT INTO dieta (nome, calorias_totais) VALUES (%s, %s)"
                values = (nome, calorias)
                cursor.execute(query, values)
                conn.commit()

                popup_sucesso = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text("Dieta cadastrada com sucesso!"),
                    actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_sucesso))]
                )
                page.overlay.append(popup_sucesso)
                popup_sucesso.open = True

                page.overlay.remove(dialogos)

        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        finally:
            cursor.close()
            conn.close()

        page.update()

    def atualizar_tabela(table):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT nome, calorias_totais FROM dieta")
            result = cursor.fetchall()

            # Limpa as linhas existentes
            table.rows.clear()

            # Adiciona as novas linhas
            for dieta in result:
                nova_linha = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(dieta[0])),
                        ft.DataCell(ft.Text(str(dieta[1]))),
                    ]
                )
                table.rows.append(nova_linha)

        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        finally:
            cursor.close()
            conn.close()

        # Atualiza a página para refletir a nova tabela
        page.update()


    def page_nutro(page: ft.Page):
        page.clean()  # Limpa a página

        def page_dietas():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT nome, calorias_totais FROM dieta")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()

            finally:
                cursor.close()
                conn.close()

            if result:
                boot1 = ft.ElevatedButton("Adicionar Dieta", icon=ft.icons.ADD, on_click=lambda e: cadastrar_dieta(page))
                boot2 = ft.ElevatedButton("Apagar Dieta", icon=ft.icons.REMOVE, on_click=lambda e: deletar_dieta(page))
                boot3 = ft.ElevatedButton("Atualizar Tabela", icon=ft.icons.REFRESH, on_click=lambda e: atualizar_tabela(table))

                title_container = ft.Container(
                    content=ft.Text("Dietas", size=30, color="white"),
                    bgcolor="#4F4F4F",
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(10)
                )

                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Nome")),
                        ft.DataColumn(ft.Text("Calorias Totais")),
                    ],
                    rows=[]
                )

                # Adiciona as dietas à tabela
                for dieta in result:
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(dieta[0])),
                            ft.DataCell(ft.Text(str(dieta[1]))),
                        ]
                    )
                    table.rows.append(nova_linha)

                table_container = ft.Container(
                    content=ft.Column(
                        controls=[table],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=300,
                    bgcolor="#4F4F4F",
                    border_radius=ft.border_radius.all(10),
                    padding=ft.padding.all(10),
                )

                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            title_container,
                            table_container,
                            ft.Row(
                                controls=[
                                    boot1,
                                    boot2,
                                    boot3,  # Adiciona o botão de atualização
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            else:
                # Caso não haja dietas
                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Nenhuma dieta a ver", size=20, color="#D3D3D3"),
                            ft.ElevatedButton("Adicionar Dieta", icon=ft.icons.ADD, on_click=lambda e: print("Botão clicado!")),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            return main_content
        
        def page_alimentos():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT nome, calorias, proteinas, carboidratos, gorduras FROM alimento")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()

            finally:
                cursor.close()
                conn.close()

            if result:
                boot1 = ft.ElevatedButton("Adicionar Alimento", icon=ft.icons.ADD, on_click=lambda e: "cadastrar_alimento(page)")
                boot2 = ft.ElevatedButton("Apagar Alimento", icon=ft.icons.REMOVE, on_click=lambda e: "deletar_alimento(page)")
                boot3 = ft.ElevatedButton("Atualizar Tabela", icon=ft.icons.REFRESH, on_click=lambda e: atualizar_tabela(table))

                title_container = ft.Container(
                    content=ft.Text("Alimentos", size=30, color="white"),
                    bgcolor="#4F4F4F",
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(10)
                )

                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Nome")),
                        ft.DataColumn(ft.Text("Calorias")),
                        ft.DataColumn(ft.Text("Proteínas")),
                        ft.DataColumn(ft.Text("Carboidratos")),
                        ft.DataColumn(ft.Text("Gorduras")),
                    ],
                    rows=[]
                )

                # Adiciona os alimentos à tabela
                for alimento in result:
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(alimento[0])),
                            ft.DataCell(ft.Text(str(alimento[1]))),
                            ft.DataCell(ft.Text(str(alimento[2]))),
                            ft.DataCell(ft.Text(str(alimento[3]))),
                            ft.DataCell(ft.Text(str(alimento[4]))),
                        ]
                    )
                    table.rows.append(nova_linha)

                table_container = ft.Container(
                    content=ft.Column(
                        controls=[table],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=300,
                    bgcolor="#4F4F4F",
                    border_radius=ft.border_radius.all(10),
                    padding=ft.padding.all(10),
                )

                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            title_container,
                            table_container,
                            ft.Row(
                                controls=[
                                    boot1,
                                    boot2,
                                    boot3,  # Adiciona o botão de atualização
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            else:
                # Caso não haja alimentos
                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Nenhum alimento a ver", size=20, color="#D3D3D3"),
                            ft.ElevatedButton("Adicionar Alimento", icon=ft.icons.ADD, on_click=lambda e: print("Botão clicado!")),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            return main_content

        # Barra lateral simulada
# Barra lateral simulada
        sidebar = build_custom_navbar(page, page_alimentos)

        # Adiciona conteúdo principal (inicialmente vazio, mas preenchido pelo retorno da função page_alimentos)
        main_content = page_alimentos()

        # Layout da página com barra lateral e conteúdo
        page_layout = ft.Row(
            [
                sidebar,  # Barra lateral à esquerda
                main_content,  # Conteúdo principal à direita
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
            spacing=250  # Adiciona um espaço fixo entre os componentes
        )

        # Adiciona o layout à página
        page.add(page_layout)
        page.update()

ft.app(target=main)