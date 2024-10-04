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
    page.window.width = 1000  # Defina uma largura adequada para sua aplicação
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

    def build_custom_navbar(page):
        def handle_nav_click(label):
            print(f"Botão {label} clicado")
            # Aqui você pode adicionar a lógica para mudar o conteúdo da página

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
                        on_click=lambda e, label=nav_item["label"]: handle_nav_click(label),
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

    def page_nutro(page: ft.Page):
        page.clean()  # Limpa a página

        # Barra lateral simulada
        sidebar = build_custom_navbar(page)

        # Container principal onde o conteúdo será adicionado no futuro
        main_content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Nenhuma dieta a ver", size=20, color="#D3D3D3"),
                    ft.ElevatedButton("Adicionar Dieta",icon=ft.icons.ADD, on_click=lambda e: print("Botão clicado!")),

                ]
            ),
            padding=ft.padding.all(20),
        )

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