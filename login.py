import flet as ft
import mysql.connector
import time

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLUE_GREY_800
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
                # O tipo de usuário está na quarta coluna (índice 3)
                tipo_usuario = result[0][4]  # Modifique o índice conforme a estrutura da sua tabela
                usuario_id = result[0][0]  # Obtenha o ID do usuário (primeira coluna)

                show_popup_login_sucesso()
                page.clean()

                if tipo_usuario.lower() == "nutrólogo":
                    page_nutro(page)
                elif tipo_usuario.lower() == "paciente":
                    # Chame a função page_paci passando o id do usuário
                    page_paci(page, usuario_id)
                else:
                    show_popup_usuario_nao_encontrado()
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

    def show_popup_imc_error():
        popup = ft.AlertDialog(
            title=ft.Text("Erro!"),
            content=ft.Text("Altura e peso devem ser números válidos e separados por ponto (.)!"),
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

    def calcular_imc(altura, peso):
        try:
            altura = float(altura.replace(",", ".").strip())
            peso = float(peso.replace(",", ".").strip())
            return round(peso / (altura ** 2), 2)
        except ValueError:
            return None

    def verificar_campos(e, label_cadastro, nome_cadastro, email_cadastro, senha_cadastro, repetir_senha, altura_cadastro, peso_cadastro, v_senha_existe):
        print("Função verificar_campos chamada")
        # Verificar se todos os campos estão preenchidos
        if any(not field.value for field in [nome_cadastro, email_cadastro, senha_cadastro, repetir_senha, altura_cadastro, peso_cadastro]):
            print("Campo vazio detectado")
            show_popup_vasio()
        # Verificar se as senhas coincidem
        elif senha_cadastro.value.strip() != repetir_senha.value.strip():
            print(f"Senha: {senha_cadastro.value}, Repetir Senha: {repetir_senha.value}")
            show_popup_cadastro_erro()
        else:
            print("Senhas coincidem, continuando o cadastro")
            imc = calcular_imc(altura_cadastro.value, peso_cadastro.value)
            if imc is None:
                show_popup_imc_error()
            else:
                verificar_email(email_cadastro, v_senha_existe, e)

    def voltar_loguin(e):
        page.controls.clear()
        page.update()
        main(page)

    def show_popup_voltar_login():
        popup = ft.AlertDialog(
            title=ft.Text("Atenção!"),
            content=ft.Text("Você deseja voltar para a tela de login?"),
            actions=[ft.TextButton("OK", on_click=lambda e: fechar_popup())],
            actions_alignment=ft.MainAxisAlignment.END
        )

        def fechar_popup():
            popup.open = False
            page.update()
            voltar_loguin(page)

        page.dialog = popup
        popup.open = True
        page.update()

    def abrir_cadastro():
        page.controls.clear()

        label_cadastro = ft.Text("Cadastro", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        nome_cadastro = ft.TextField(label="Nome")
        email_cadastro = ft.TextField(label="Email")
        senha_cadastro = ft.TextField(label="Senha", password=True)
        repetir_senha = ft.TextField(label="Repetir Senha", password=True)
        altura_cadastro = ft.TextField(label="Informe sua altura (ex: 1.75)")
        peso_cadastro = ft.TextField(label="Informe seu peso (ex: 73.5)")
        botao_voltar = ft.ElevatedButton(text="X", on_click= voltar_loguin)

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
                    # Se a senha já existe no banco, chama o popup de senha existente e interrompe o cadastro
                    if resultado[0] == senha_cadastro.value:
                        senha_existe()
                        return

                # Determina se o usuário é Nutrólogo ou Paciente
                if radio_group.value == 'Nutrólogo':
                    tipo_usuario = "Nutrólogo"
                elif radio_group.value == 'Paciente':
                    tipo_usuario = "Paciente"
                else:
                    tipo_usuario = None  # Caso queira adicionar algum tratamento para outros casos

                # Calcula o IMC e insere o novo usuário no banco
                imc = calcular_imc(altura_cadastro.value, peso_cadastro.value)
                cursor.execute(
                    "INSERT INTO usuario (nome, email, senha, imc, tipo) VALUES (%s, %s, %s, %s, %s)",
                    (nome_cadastro.value, email_cadastro.value, senha_cadastro.value, imc, tipo_usuario)
                )
                conn.commit()

                # Após cadastro bem-sucedido, exibe o popup de sucesso
                show_popup_cadastro_sucesso()

                # Opcional: Redirecionar para a tela de login após o cadastro
                voltar_para_login()

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
                    ft.Radio(value="Paciente", label="Paciente")
                ]
            )
        )

        botao_cadastrar = ft.ElevatedButton(
            text="Cadastrar",
            on_click=lambda e: verificar_campos(
                e, label_cadastro, nome_cadastro, email_cadastro, senha_cadastro, repetir_senha, altura_cadastro, peso_cadastro, v_senha_existe
            )
        )

        frame_cadastro = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(label_cadastro, alignment=ft.alignment.center, bgcolor="#4D4D4D", padding=18),
                            ft.Container(nome_cadastro, alignment=ft.alignment.center),
                            ft.Container(email_cadastro, alignment=ft.alignment.center),
                            ft.Container(senha_cadastro, alignment=ft.alignment.center),
                            ft.Container(repetir_senha, alignment=ft.alignment.center),
                            ft.Container(altura_cadastro, alignment=ft.alignment.center),
                            ft.Container(peso_cadastro, alignment=ft.alignment.center),
                            ft.Container(radio_group, alignment=ft.alignment.center),
                            ft.Container(botao_cadastrar, alignment=ft.alignment.center),
                            ft.Container(botao_voltar, alignment=ft.alignment.bottom_right,),
                        ]
                    ),
                    bgcolor="#696969",
                    width=400,
                    height=600,
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



    page.title = "Healthy Vision"
    page.window.full_screen = False  # Muda para False para não ser tela cheia
    page.window.width = 1250  # Defina uma largura adequada para sua aplicação
    page.window.height = 970  # Defina uma altura adequada para sua aplicação

    label = ft.Text("Healthy Vision", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
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

    def deletar_dieta(page: ft.Page):
        nome_field = ft.TextField(label="Nome da dieta a ser deletada:")

        dialogo_deletar = ft.AlertDialog(
            title=ft.Text("Deletar Dieta"),
            content=ft.Column([nome_field]),
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
                show_success_popup("Dieta deletada com sucesso!", page, dialogo_deletar)
                atualizar_tabela(table)
            else:
                show_error_popup("Dieta não encontrada.", page)

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao tentar deletar a dieta.", page)

        finally:
            cursor.close()
            conn.close()

    def cadastrar_alimento(page: ft.Page):
        nome_field = ft.TextField(label="Nome do alimento:")
        calorias_field = ft.TextField(label="Calorias:", keyboard_type=ft.KeyboardType.NUMBER)
        pro_field = ft.TextField(label="Proteínas:", keyboard_type=ft.KeyboardType.NUMBER)
        carbo_field = ft.TextField(label="Carboidratos:", keyboard_type=ft.KeyboardType.NUMBER)
        gordu_field = ft.TextField(label="Gorduras:", keyboard_type=ft.KeyboardType.NUMBER)

        dialogos = ft.AlertDialog(
            title=ft.Text("Cadastrar Alimento"),
            content=ft.Column([nome_field, calorias_field, pro_field, carbo_field, gordu_field]),
            actions=[
                ft.ElevatedButton(
                    text='Cadastrar',
                    on_click=lambda e: inserir_alimento(nome_field.value, calorias_field.value, pro_field.value, carbo_field.value, gordu_field.value, dialogos, page)
                ),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: page.overlay.remove(dialogos)),
            ]
        )

        page.overlay.append(dialogos)
        dialogos.open = True
        page.update()

    def inserir_alimento(nome, calorias, pro, carbo, gordu, dialogos, page):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT nome FROM alimento WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                show_error_popup("Esse alimento já existe.", page)
            else:
                query = "INSERT INTO alimento (nome, calorias, proteinas, carboidratos, gorduras) VALUES (%s, %s, %s, %s, %s)"
                values = (nome, calorias, pro, carbo, gordu)
                cursor.execute(query, values)
                conn.commit()
                show_success_popup("Alimento cadastrado com sucesso!", page, dialogos)
                atualizar_tabela_a(table)

                dialogos.open = False
                page.overlay.remove(dialogos)
                page.update()

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao cadastrar o alimento.", page)

        finally:
            cursor.close()
            conn.close()

    def show_success_popup(message, page, dialog=None):
        popup_sucesso = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text(message),
            actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_sucesso))]
        )
        page.overlay.append(popup_sucesso)
        popup_sucesso.open = True
        if dialog:
            page.overlay.remove(dialog)
        page.update()

    def show_error_popup(message, page):
        popup_erro = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(message),
            actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_erro))]
        )
        page.overlay.append(popup_erro)
        popup_erro.open = True
        page.update()

    def atualizar_tabela_a(table):
        print("chegou")
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )

            if conn.is_connected():
                cursor = conn.cursor()

                cursor.execute("SELECT id, nome, calorias, proteinas, carboidratos, gorduras FROM alimento")
                result = cursor.fetchall()

                table.rows.clear()

                for alimento in result:
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(alimento[0])),  # Nome do alimento
                            ft.DataCell(ft.Text(str(alimento[1]))),  # Calorias totais
                            ft.DataCell(ft.Text(str(alimento[2]))),  # Proteínas
                            ft.DataCell(ft.Text(str(alimento[3]))),  # Carboidratos
                            ft.DataCell(ft.Text(str(alimento[4]))),
                            ft.DataCell(ft.Text(str(alimento[5]))),
                        ]
                    )
                    table.rows.append(nova_linha)

                table.update()

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao atualizar a tabela.", page)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            show_error_popup("Erro inesperado ao atualizar a tabela.", page)

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                
    def atualizar_tabela_b(table):
        print("chegou")
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )

            if conn.is_connected():
                cursor = conn.cursor()

                cursor.execute("SELECT id_refeicao, id_alimento, quantidade, tipo_medida, horario FROM refeicao_alimento")
                result = cursor.fetchall()

                table.rows.clear()

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


                table.update()

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao atualizar a tabela.", page)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            show_error_popup("Erro inesperado ao atualizar a tabela.", page)

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def deletar_alimento_a(page: ft.Page):
        nome_field = ft.TextField(label="Nome do alimento a ser deletado:")

        dialogo_deletar = ft.AlertDialog(
            title=ft.Text("Deletar Alimento"),
            content=ft.Column([nome_field]),
            actions=[
                ft.ElevatedButton(
                    text='Deletar',
                    on_click=lambda e: remover_alimento_a(nome_field.value, dialogo_deletar, page)
                ),
                ft.ElevatedButton(text='Cancelar', on_click=lambda e: page.overlay.remove(dialogo_deletar)),
            ]
        )

        page.overlay.append(dialogo_deletar)
        dialogo_deletar.open = True
        page.update()
        

    def remover_alimento_a(nome, dialogo_deletar, page):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT nome FROM alimento WHERE nome = %s", (nome,))
            resultado = cursor.fetchone()

            if resultado:
                cursor.execute("DELETE FROM alimento WHERE nome = %s", (nome,))
                conn.commit()
                show_success_popup("Alimento deletado com sucesso!", page, dialogo_deletar)
                atualizar_tabela_a(table)
            else:
                show_error_popup("Alimento não encontrado.", page)  # Correção da mensagem de erro

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao tentar deletar o alimento.", page)  # Correção da mensagem

        finally:
            cursor.close()
            conn.close()

    def cadastrar_dieta(page: ft.Page):
        nome_field = ft.TextField(label="Nome da dieta:")
        calorias_field = ft.TextField(label="Calorias Totais:", keyboard_type=ft.KeyboardType.NUMBER)

        dialogos = ft.AlertDialog(
            title=ft.Text("Cadastrar Dieta"),
            content=ft.Column([nome_field, calorias_field]),
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
                show_error_popup("Essa dieta já existe.", page)
            else:
                query = "INSERT INTO dieta (nome, calorias_totais) VALUES (%s, %s)"
                values = (nome, calorias)
                cursor.execute(query, values)
                conn.commit()
                show_success_popup("Dieta cadastrada com sucesso!", page, dialogos)
                atualizar_tabela(table)

        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao cadastrar a dieta.", page)

        finally:
            cursor.close()
            conn.close()

    def show_success_popup(message, page, dialog=None):
        popup_sucesso = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text(message),
            actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_sucesso))]
        )
        page.overlay.append(popup_sucesso)
        popup_sucesso.open = True
        if dialog:
            page.overlay.remove(dialog)
        page.update()

    def show_error_popup(message, page):
        popup_erro = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(message),
            actions=[ft.ElevatedButton(text="Ok", on_click=lambda e: page.overlay.remove(popup_erro))]
        )
        page.overlay.append(popup_erro)
        popup_erro.open = True
        page.update()

    def atualizar_tabela(table):
        print("chegou")
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, calorias_totais FROM dieta")
            result = cursor.fetchall()

            table.rows.clear()

            for dieta in result:
                nova_linha = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(dieta[0]))),  # id
                        ft.DataCell(ft.Text(dieta[1])),  # Nome
                        ft.DataCell(ft.Text(str(dieta[2]))),  # Calorias
                    ]
                )
                table.rows.append(nova_linha)
                table.update()

        except mysql.connector.Error as err:
            print(f"Erro: {err}")

        finally:
            cursor.close()
            conn.close()

    def show_tutorial(page):
        def close_popup(e):
            page.dialog.open = False
            page.update()

        tutorial = ft.AlertDialog(
            title=ft.Text("Tutorial de Cadastro de Refeição"),
            content=ft.Text(
                "Para adicionar uma refeição, siga as etapas:\n\n"
                "1. Selecione a refeição (Café da manhã, Almoço, etc.) e horário.\n"
                "2. Selecione a dieta a ser associada.\n"
                "3. Selecione os alimentos e adicione a quantidade e a medida de cada um.\n"
                "4. Clique em Confirmar para salvar."
            ),
            actions=[ft.TextButton("Fechar", on_click=close_popup)],
        )
        show_cadastro_refeicao(page)  # Mostra a tela de cadastro de refeição
        page.dialog = tutorial  # Define o tutorial como um diálogo popup
        page.dialog.open = True  # Abre o popup
        page.update()


    def show_cadastro_refeicao(page):
        dietas = buscar_dietas()  # Busca as dietas disponíveis no banco de dados

        # Cria um dropdown para selecionar a refeição
        dropdown_refeicao = ft.Dropdown(
            label="Selecione a Refeição",
            options=[
                ft.dropdown.Option("Café da manhã"),
                ft.dropdown.Option("Almoço"),
                ft.dropdown.Option("Jantar"),
                ft.dropdown.Option("Lanche")
            ]
        )

        input_horario = ft.TextField(label="Horário (HH:MM)")  # Campo de texto para o horário

        # Cria um dropdown para selecionar a dieta
        dropdown_dieta = ft.Dropdown(
            label="Selecione a Dieta",
            options=[
                ft.dropdown.Option(str(dieta[0]), dieta[1]) for dieta in dietas
            ]
        )

        # Função para confirmar a refeição e passar para a próxima tela
        def confirmar_refeicao(e):
            nome_refeicao = dropdown_refeicao.value
            horario = input_horario.value
            id_dieta = dropdown_dieta.value

            # Validação básica para verificar se os campos estão preenchidos
            if nome_refeicao and horario and id_dieta:
                id_refeicao = cadastrar_refeicao(nome_refeicao, horario, id_dieta)
                if id_refeicao:
                    show_cadastro_alimento(page, id_refeicao)
                    
                    # Limpar os campos após o cadastro
                    dropdown_refeicao.value = None
                    input_horario.value = ""
                    dropdown_dieta.value = None

                    # Atualiza a página para refletir as alterações
                    page.update()
            else:
                print("Preencha todos os campos!")

        # Adiciona os componentes à página
        page.add(
            dropdown_refeicao,
            input_horario,
            dropdown_dieta,
            ft.ElevatedButton("Confirmar", on_click=confirmar_refeicao)
        )


    # Função para buscar dietas no banco de dados
    def buscar_dietas():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM dieta")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            return []
        finally:
            cursor.close()
            conn.close()


    # Função para cadastrar a refeição no banco de dados
    def cadastrar_refeicao(nome, horario, id_dieta):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO refeicao (nome, horario, dieta)
                VALUES (%s, %s, %s)
            """, (nome, horario, int(id_dieta)))
            conn.commit()
            atualizar_tabela_b(table)
            return cursor.lastrowid  # Retorna o ID da refeição criada
        except mysql.connector.Error as err:
            print(f"Erro ao cadastrar refeição: {err}")
            return None
        finally:
            cursor.close()
            conn.close()


    # Função para mostrar o cadastro de alimentos após a refeição ter sido cadastrada
    def show_cadastro_alimento(page, id_refeicao):
        alimentos = buscar_alimentos()  # Busca os alimentos no banco de dados

        # Cria uma tabela para exibir os alimentos disponíveis
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Calorias")),
                ft.DataColumn(ft.Text("Adicionar")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(alimento[0]))),
                        ft.DataCell(ft.Text(alimento[1])),
                        ft.DataCell(ft.Text(str(alimento[2]))),
                        ft.DataCell(ft.IconButton(
                            icon=ft.icons.ADD,
                            on_click=lambda e, id_alimento=alimento[0]: adicionar_quantidade_medida(page, id_alimento, id_refeicao)
                        )),
                    ]
                ) for alimento in alimentos
            ]
        )

        # Mostra o formulário em um popup com uma barra de rolagem
        form = ft.AlertDialog(
            title=ft.Text("Cadastro de Alimentos"),
            content=ft.Container(
                content=ft.Column([table], scroll=ft.ScrollMode.AUTO),
                width=500, height=300  # Define um tamanho fixo para a barra de rolagem
            ),
            actions=[
                ft.TextButton("Concluir", on_click=lambda e: page.dialog.close()),
                ft.TextButton("Cancelar", on_click=lambda e: page.dialog.close())
            ]
        )

        page.dialog = form
        page.dialog.open = True  # Abre o popup
        page.update()


    # Função para buscar os alimentos no banco de dados
    def buscar_alimentos():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, calorias FROM alimento")
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro ao buscar alimentos: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    def buscar_medidas():
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT id, tipo_quan FROM medida")
            return [
                ft.dropdown.Option(str(medida[0]), medida[1]) for medida in cursor.fetchall()
            ]
        except mysql.connector.Error as err:
            print(f"Erro ao buscar medidas: {err}")
            return []
        finally:
            cursor.close()
            conn.close()

    # Função para adicionar a quantidade e a medida de um alimento
    def adicionar_quantidade_medida(page, id_alimento, id_refeicao):
        dropdown_medida = ft.Dropdown(label="Selecione a Medida", options=buscar_medidas())  # Busca as medidas
        input_quantidade = ft.TextField(label="Quantidade")

        # Popup para adicionar a quantidade
        popup = ft.AlertDialog(
            title=ft.Text("Adicionar Quantidade"),
            content=ft.Column([dropdown_medida, input_quantidade]),
            actions=[
                ft.TextButton("Adicionar", on_click=lambda e: confirmar_quantidade_medida(page, input_quantidade, dropdown_medida, id_alimento, id_refeicao)),
                ft.TextButton("Cancelar", on_click=lambda e: close_popup(page, id_refeicao))
            ]
        )

        page.dialog = popup
        page.dialog.open = True  # Abre o popup
        page.update()

    # Função para confirmar a quantidade e salvar no banco de dados
    def confirmar_quantidade_medida(page, input_quantidade, dropdown_medida, id_alimento, id_refeicao):
        quantidade = input_quantidade.value
        id_medida = dropdown_medida.value

        if quantidade and id_medida:
            try:
                # Verifica se a quantidade é um número
                if not quantidade.isdigit():
                    print("Por favor, insira uma quantidade válida.")
                    return
                
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()

                # Converte a quantidade para inteiro
                quantidade_int = int(quantidade)

                cursor.execute("""
                    INSERT INTO refeicao_alimento (id_refeicao, id_alimento, quantidade, tipo_medida)
                    VALUES (%s, %s, %s, %s)
                """, (id_refeicao, id_alimento, quantidade_int, id_medida))  # O id_medida deve ser um valor que existe na tabela medida
                conn.commit()
                print(f"Alimento adicionado: ID {id_alimento}, Quantidade: {quantidade_int}, ID Medida: {id_medida}")
            except mysql.connector.Error as err:
                print(f"Erro ao salvar refeicao_alimento: {err}")
            finally:
                cursor.close()
                conn.close()

            # Fechar o popup e reabrir a tabela de alimentos
            close_popup(page, id_refeicao)
        else:
            print("Por favor, preencha todos os campos antes de confirmar.")


    # Função para fechar o popup e reabrir a tela de cadastro de alimentos
    def close_popup(page, id_refeicao):
        page.dialog.open = False  # Fecha o popup atual
        page.update()

        # Reabre o cadastro de alimentos para a mesma refeição
        show_cadastro_alimento(page, id_refeicao)


    def show_dialog_delete_refeicao():
        dialog = ft.AlertDialog(
            title=ft.Text("Apagar Refeição"),
            content=ft.TextField(label="ID da refeição para apagar"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: dialog.dismiss()),
                ft.TextButton("Confirmar", on_click=lambda e: delete_refeicao(dialog))
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def delete_refeicao(dialog):
        id_refeicao = dialog.content.controls[0].value

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM refeicao_alimento WHERE id_refeicao = %s", (id_refeicao,))
            conn.commit()
            show_success_popup("Refeição apagada com sucesso!")
            atualizar_tabela_b(table)
        except mysql.connector.Error as err:
            print(f"Erro: {err}")
            show_error_popup("Erro ao apagar a refeição.")
        finally:
            cursor.close()
            conn.close()
        dialog.dismiss()
        
    def enviar_dieta_dialog():
        # Conectar ao banco de dados e obter dietas e usuários
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            cursor = conn.cursor()

            # Obter dietas da tabela dieta
            cursor.execute("SELECT id, nome FROM dieta")
            dietas = cursor.fetchall()

            # Obter usuários com status de "paciente"
            cursor.execute("SELECT id, nome FROM usuario WHERE tipo = 'paciente'")
            usuarios = cursor.fetchall()

        except mysql.connector.Error as err:
            ft.dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text(f"Erro ao conectar ao banco de dados: {err}"),
                actions=[ft.ElevatedButton("OK", on_click=lambda e: page.overlay.remove(dialog))]
            )
            page.overlay.append(ft.dialog)
            page.update()
            return

        finally:
            cursor.close()
            conn.close()

        # Dropdown para selecionar dieta
        dropdown_dieta = ft.Dropdown(
            label="Selecione a Dieta",
            options=[ft.dropdown.Option(str(dieta[0]), dieta[1]) for dieta in dietas]
        )

        # Dropdown para selecionar usuário
        dropdown_usuario = ft.Dropdown(
            label="Selecione o Usuário",
            options=[ft.dropdown.Option(str(usuario[0]), usuario[1]) for usuario in usuarios]
        )

        # Função para salvar a dieta selecionada no usuário
        def salvar_dieta(e):
            dieta_id = dropdown_dieta.value
            usuario_id = dropdown_usuario.value

            if not dieta_id or not usuario_id:
                ft.dialog = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text("Por favor, selecione uma dieta e um usuário"),
                    actions=[ft.ElevatedButton("OK", on_click=lambda e: page.overlay.remove(dialog))]
                )
                page.overlay.append(ft.dialog)
                page.update()
                return

            # Atualizar a tabela usuario com a dieta selecionada
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                # Atualizar o usuário com a dieta selecionada
                cursor.execute("UPDATE usuario SET dieta = %s WHERE id = %s", (dieta_id, usuario_id))
                conn.commit()

                # Popup de sucesso
                ft.dialog = ft.AlertDialog(
                    title=ft.Text("Sucesso"),
                    content=ft.Text("Dieta atribuída ao usuário com sucesso!"),
                    actions=[ft.ElevatedButton("OK", on_click=lambda e: page.overlay.remove(ft.dialog))]
                )
                page.overlay.append(ft.dialog)
                page.update()

            except mysql.connector.Error as err:
                ft.dialog = ft.AlertDialog(
                    title=ft.Text("Erro"),
                    content=ft.Text(f"Erro ao salvar dieta: {err}"),
                    actions=[ft.ElevatedButton("OK", on_click=lambda e: page.overlay.remove(dialog))]
                )
                page.overlay.append(ft.dialog)
                page.update()

            finally:
                cursor.close()
                conn.close()
                # Não fechar o diálogo aqui, apenas removê-lo após a ação

        # Criar o AlertDialog com os dois dropdowns
        dialog = ft.AlertDialog(
            title=ft.Text("Atribuir Dieta ao Usuário"),
            content=ft.Column(
                controls=[
                    dropdown_dieta,
                    dropdown_usuario,
                    ft.ElevatedButton("Salvar", on_click=salvar_dieta)
                ]
            ),
            actions=[
                ft.ElevatedButton("Cancelar", on_click=lambda e: page.overlay.remove(dialog))  # Fecha o diálogo de atribuição
            ]
        )

        # Adiciona o diálogo à lista de overlays da página e o abre
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    def page_nutro(page: ft.Page):
        def page_dietas():
            page.clean()
            page.add(tabs)

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas", 
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, calorias_totais FROM dieta")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_error_popup("Erro ao carregar as dietas.", page)
                result = []

            finally:
                cursor.close()
                conn.close()

            if result:
                setup_dietas_page(page, result)
            else:
                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Nenhuma dieta a ver", size=20, color="#D3D3D3"),
                            ft.ElevatedButton("Adicionar dieta", icon=ft.icons.ADD, on_click=lambda e: cadastrar_dieta(page)),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )
                
                return main_content

        def setup_dietas_page(page, result):
            global table
            search_field = ft.TextField(label="Pesquisar Dieta", on_change=lambda e: update_dietas_table(e.control.value))

            boot1 = ft.ElevatedButton("Adicionar Dieta", icon=ft.icons.ADD, on_click=lambda e: cadastrar_dieta(page))
            boot2 = ft.ElevatedButton("Apagar Dieta", icon=ft.icons.REMOVE, on_click=lambda e: deletar_dieta(page))
            boot3 = ft.ElevatedButton("Enviar dieta", icon=ft.icons.REFRESH, on_click=lambda e: enviar_dieta_dialog())

            title_container = ft.Container(
                content=ft.Text("Dietas", size=30, color="white"),
                bgcolor="#4F4F4F",
                padding=ft.padding.all(20),
                alignment=ft.alignment.center,
                border_radius=ft.border_radius.all(10)
            )

            table = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("id")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Calorias Totais")),
                ],
                rows=[]
            )

            for dieta in result:
                nova_linha = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(int(dieta[0]))),
                        ft.DataCell(ft.Text(str(dieta[1]))),
                        ft.DataCell(ft.Text(str(dieta[2]))),
                    ]
                )
                table.rows.append(nova_linha)

            table_container = ft.Container(
                content=ft.Column(
                    controls=[
                        search_field,
                        ft.Row(controls=[table], alignment=ft.MainAxisAlignment.CENTER)
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                height=300,
                bgcolor="#4F4F4F",
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(10),
            )

            page.add(
                title_container,
                table_container,
                ft.Row(
                    controls=[boot1, boot2, boot3],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
            )

        def update_dietas_table(search_value):
            global table
            filtered_rows = []
            search_value = search_value.lower()

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, calorias_totais FROM dieta")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return

            finally:
                cursor.close()
                conn.close()

            for dieta in result:
                if search_value in dieta[1].lower():
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(dieta[0]))),  # id
                            ft.DataCell(ft.Text(dieta[1])),  # Nome
                            ft.DataCell(ft.Text(str(dieta[2]))),  # Calorias
                        ]
                    )
                    filtered_rows.append(nova_linha)

            table.rows = filtered_rows
            table.update()

        table = None  # Inicializa como None

        def page_alimentos():
            global table

            # Conectar ao banco de dados e buscar alimentos
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, calorias, proteinas, carboidratos, gorduras FROM alimento")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()
                return ft.Container()  # Retorna um contêiner vazio em caso de erro

            finally:
                cursor.close()
                conn.close()

            # Definindo a tabela e o campo de pesquisa
            if result:
                # Criar o campo de pesquisa
                search_field = ft.TextField(label="Pesquisar Alimento", on_change=lambda e: update_table(e.control.value))

                boot1 = ft.ElevatedButton("Adicionar Alimento", icon=ft.icons.ADD, on_click=lambda e: cadastrar_alimento(page))
                boot2 = ft.ElevatedButton("Apagar Alimento", icon=ft.icons.REMOVE, on_click=lambda e: deletar_alimento_a(page))

                title_container = ft.Container(
                    content=ft.Text("Alimentos", size=30, color="white"),
                    bgcolor="#4F4F4F",
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(10)
                )

                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
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
                            ft.DataCell(ft.Text(str(alimento[5]))),
                        ]
                    )
                    table.rows.append(nova_linha)

                table_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            search_field,
                            ft.Row(controls=[table], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=300,
                    bgcolor="#4F4F4F",
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                )

                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            title_container,
                            table_container,
                            ft.Row(
                                controls=[boot1, boot2],
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
                            ft.ElevatedButton("Adicionar Alimento", icon=ft.icons.ADD, on_click=lambda e: cadastrar_alimento(page)),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            return main_content

        def update_table(search_value):
            global table  # Acessa a tabela como global
            # Filtra a tabela com base no valor da pesquisa
            filtered_rows = []
            search_value = search_value.lower()  # Normaliza a busca para letras minúsculas

            # Realiza a consulta ao banco de dados para obter os alimentos
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, calorias, proteinas, carboidratos, gorduras FROM alimento")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return

            finally:
                cursor.close()
                conn.close()

            # Filtra os resultados de acordo com a pesquisa
            for alimento in result:
                if search_value in alimento[1].lower():  # Verifica se o nome do alimento contém o valor da pesquisa
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(alimento[0])),  # ID
                            ft.DataCell(ft.Text(str(alimento[1]))),
                            ft.DataCell(ft.Text(str(alimento[2]))),
                            ft.DataCell(ft.Text(str(alimento[3]))),
                            ft.DataCell(ft.Text(str(alimento[4]))),
                            ft.DataCell(ft.Text(str(alimento[5]))),
                        ]
                    )
                    filtered_rows.append(nova_linha)

            table.rows = filtered_rows
            table.update()
            
        def page_refeicoes():
            global table

            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, horario, dieta FROM refeicao")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                show_popup_cadastro_erro()
                return ft.Container()  # Retorna um contêiner vazio em caso de erro

            finally:
                cursor.close()
                conn.close()

            if result:
                search_field = ft.TextField(label="Pesquisar refeição por ID ou Alimento", on_change=lambda e: update_table(e.control.value))

                boot1 = ft.ElevatedButton("Adicionar refeição", icon=ft.icons.ADD, on_click=lambda e: show_tutorial(page))
                boot2 = ft.ElevatedButton("Apagar refeição", icon=ft.icons.REMOVE, on_click=lambda e: show_dialog_delete_refeicao())

                title_container = ft.Container(
                    content=ft.Text("Refeição", size=30, color="white"),
                    bgcolor="#4F4F4F",
                    padding=ft.padding.all(20),
                    alignment=ft.alignment.center,
                    border_radius=ft.border_radius.all(10)
                )

                table = ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("id")),
                        ft.DataColumn(ft.Text("nome")),
                        ft.DataColumn(ft.Text("horário")),
                        ft.DataColumn(ft.Text("dieta")),
                    ],
                    rows=[]
                )

                for alimento in result:
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(alimento[0])),
                            ft.DataCell(ft.Text(alimento[1])),
                            ft.DataCell(ft.Text(alimento[2])),
                            ft.DataCell(ft.Text(alimento[3])),
                        ]
                    )
                    table.rows.append(nova_linha)

                table_container = ft.Container(
                    content=ft.Column(
                        controls=[
                            search_field,
                            ft.Row(controls=[table], alignment=ft.MainAxisAlignment.CENTER)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    height=300,
                    bgcolor="#4F4F4F",
                    padding=ft.padding.all(10),
                    border_radius=ft.border_radius.all(10),
                )

                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            title_container,
                            table_container,
                            ft.Row(
                                controls=[boot1, boot2],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            else:
                main_content = ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Nenhuma refeição a ver", size=20, color="#D3D3D3"),
                            ft.ElevatedButton("Adicionar Refeição", icon=ft.icons.ADD, on_click=lambda e: show_tutorial(page)),
                            ft.ElevatedButton("Atualizar página", icon=ft.icons.REFRESH, on_click=lambda e: atualizar_tabela_b(table))
                        ]
                    ),
                    padding=ft.padding.all(20),
                )

            return main_content

        def update_table(search_value):
            global table  # Acessa a tabela como global
            filtered_rows = []
            search_value = search_value.lower()  # Normaliza a busca para letras minúsculas

            # Realiza a consulta ao banco de dados para obter as refeições
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="acesso123",
                    database="dietas",
                    port="3306"
                )
                cursor = conn.cursor()
                cursor.execute("SELECT id, nome, horario, dieta FROM refeicao")
                result = cursor.fetchall()

            except mysql.connector.Error as err:
                print(f"Erro: {err}")
                return

            finally:
                cursor.close()
                conn.close()

            # Filtra os resultados de acordo com o valor da pesquisa
            for refeicao in result:
                id_refeicao = str(refeicao[0])  # Converte o id para string para facilitar a busca
                nome_refeicao = refeicao[1].lower()  # Converte o nome para letras minúsculas

                # Verifica se o ID ou o nome da refeição contém o valor da pesquisa
                if search_value in id_refeicao or search_value in nome_refeicao:
                    nova_linha = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(refeicao[0]))),  # ID
                            ft.DataCell(ft.Text(refeicao[1])),  # Nome
                            ft.DataCell(ft.Text(refeicao[2])),  # Horário
                            ft.DataCell(ft.Text(refeicao[3]))  # Dieta
                        ]
                    )
                    filtered_rows.append(nova_linha)

            # Atualiza a tabela com os resultados filtrados
            table.rows = filtered_rows
            table.update()

        def tab_click(e):
            page.clean()
            page.add(tabs)  # Apenas adiciona as abas

            selected_index = e.control.selected_index
            if selected_index == 0:
                page_dietas()
            elif selected_index == 1:
                main_content = page_alimentos()
                page.add(main_content)
            elif selected_index == 2:
                main_content = page_refeicoes()
                page.add(main_content)

            # Adiciona o botão "Voltar ao Login" que chama o popup
            voltar_button = ft.ElevatedButton("Voltar ao Login", on_click=lambda e: show_popup_voltar_login())
            page.add(voltar_button)

        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="Dietas", icon=ft.icons.FOOD_BANK),
                ft.Tab(text="Alimentos", icon=ft.icons.RESTAURANT),
                ft.Tab(text="Refeições", icon=ft.icons.DINNER_DINING)
            ],
            on_change=tab_click
        )

        page.add(tabs)
        page_dietas()
        
    def conectar_banco_dados():
        try:
                # Para MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="acesso123",
                database="dietas",
                port="3306"
            )
            return conn
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
            
    def page_paci(page: ft.Page, usuario_id: int):
        # Conecte-se ao banco de dados
        conn = conectar_banco_dados()
        if conn is None:
            aviso_container = ft.Container(
                content=ft.Text("Erro ao conectar ao banco de dados!", size=20, color="red"),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20)
            )
            page.add(aviso_container)
            return

        cursor = conn.cursor()

        try:
            # Busque a dieta do usuário
            cursor.execute("SELECT dieta, imc FROM usuario WHERE id = %s", (usuario_id,))
            usuario_info = cursor.fetchone()

            if usuario_info:
                dieta_id, imc = usuario_info  # Obtenha o ID da dieta e o IMC

                # Busque o nome da dieta
                cursor.execute("SELECT nome, calorias_totais FROM dieta WHERE id = %s", (dieta_id,))
                dieta_info = cursor.fetchone()

                if dieta_info:
                    dieta_nome, calorias_totais = dieta_info  # Obtenha o nome e as calorias da dieta

                    # Busque as refeições da dieta
                    cursor.execute("SELECT id, nome, horario FROM refeicao WHERE Dieta = %s", (dieta_id,))
                    refeicoes = cursor.fetchall()  # Inicializa a variável aqui

                    # Limpe a página antes de adicionar novos conteúdos
                    page.clean()

                    # Crie um container com fundo cinza
                    title_container = ft.Container(
                        content=ft.Text("Sua Dieta", size=24, weight="bold", color="blue"),
                        alignment=ft.alignment.center
                    )

                    # Adicione o botão de voltar
                    voltar_button = ft.ElevatedButton(
                        text="Voltar",
                        on_click=lambda e: show_popup_voltar_login()  # Substitua aqui com a lógica para voltar à página anterior
                    )

                    dieta_info_container = ft.Column(
                        controls=[
                            ft.Row([ft.Text("Nome da Dieta:", size=18, weight="bold"), ft.Text(dieta_nome, size=18)]),
                            ft.Row([ft.Text("Calorias Totais:", size=18, weight="bold"), ft.Text(str(calorias_totais), size=18)]),
                            ft.Divider(),
                            ft.Text("Refeições:", size=20, weight="bold")
                        ]
                    )

                    # Crie o container principal com altura fixa
                    container = ft.Container(
                        content=ft.Column(
                            controls=[title_container, voltar_button, dieta_info_container],
                            scroll=ft.ScrollMode.AUTO,  # Habilitar a rolagem automática aqui
                        ),
                        bgcolor="#4F4F4F",
                        padding=ft.padding.all(20),
                        margin=ft.margin.all(10),
                        border_radius=10,
                        height=400  # Defina uma altura fixa para o container
                    )

                    # Se houver refeições, adicione-as ao container
                    if refeicoes:  # Verifica se há refeições
                        for refeicao in refeicoes:
                            id_refeicao, nome_refeicao, horario_refeicao = refeicao
                            refeicao_info = ft.Column(
                                controls=[ft.Text(f"Refeição: {nome_refeicao} (Horário: {horario_refeicao})", size=18)]
                            )

                            # Busque os alimentos dessa refeição
                            cursor.execute("""
                                SELECT a.nome, ra.quantidade, m.tipo_quan 
                                FROM refeicao_alimento ra 
                                JOIN alimento a ON ra.id_alimento = a.id 
                                JOIN medida m ON ra.tipo_medida = m.id 
                                WHERE ra.id_refeicao = %s
                            """, (id_refeicao,))
                            alimentos = cursor.fetchall()

                            if alimentos:  # Verifica se há alimentos para a refeição
                                for alimento in alimentos:
                                    nome_alimento, quantidade, tipo_medida = alimento
                                    refeicao_info.controls.append(ft.Text(f"  - {nome_alimento}: {quantidade} {tipo_medida}", size=16))
                            else:
                                refeicao_info.controls.append(ft.Text("  - Nenhum alimento encontrado para esta refeição.", size=16, color="orange"))

                            # Adicione a refeição ao container principal
                            container.content.controls.append(refeicao_info)  # Adicione à lista de controles

                    else:
                        dieta_info_container.controls.append(ft.Text("Nenhuma refeição encontrada para esta dieta.", size=16, color="orange"))

                    # Adicione o container da dieta à página
                    page.add(container)

                    # Adicione o container "Dietas Recomendadas"
                    recomendacoes_container = ft.Column(
                        controls=[
                            ft.Text("Dietas Recomendadas", size=24, weight="bold", color="blue"),
                            ft.Text("Atenção, são só recomendações, para mais informações, converse com um nutrólogo.", size=16),
                            ft.Divider()
                        ]
                    )

                    # Calcular as calorias recomendadas
                    calorias_recomendadas = calcular_calorias_recomendadas(imc)

                    # Busque as dietas recomendadas com base nas calorias
                    cursor.execute("SELECT nome FROM dieta WHERE calorias_totais <= %s", (calorias_recomendadas,))  # Ajuste a lógica conforme necessário
                    dietas_recomendadas = cursor.fetchall()

                    if dietas_recomendadas:
                        for dieta in dietas_recomendadas:
                            nome_dieta = dieta[0]
                            recomendacoes_container.controls.append(ft.Text(f"- {nome_dieta}", size=18))
                    else:
                        recomendacoes_container.controls.append(ft.Text("Nenhuma dieta recomendada para o seu IMC.", size=16, color="orange"))

                    # Adicione o container de recomendações à página
                    page.add(recomendacoes_container)

                else:
                    aviso_container = ft.Container(
                        content=ft.Text("Dieta não encontrada!", size=20, color="red"),
                        alignment=ft.alignment.center,
                        padding=ft.padding.all(20)
                    )
                    page.add(aviso_container)
            else:
                aviso_container = ft.Container(
                    content=ft.Text("Nenhuma dieta para você!", size=20, color="red"),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20)
                )
                page.add(aviso_container)

        except mysql.connector.Error as err:
            print(f"Erro ao acessar os dados: {err}")
            aviso_container = ft.Container(
                content=ft.Text("Erro ao acessar os dados!", size=20, color="red"),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20)
            )
            page.add(aviso_container)

        finally:
            cursor.close()
            conn.close()

    def calcular_calorias_recomendadas(imc):
        # Exemplo simples de cálculo de calorias com base no IMC
        # Isso deve ser ajustado de acordo com as diretrizes nutricionais
        # Aqui, definimos uma média de 2000 calorias para um IMC normal
        calorias_base = 2000  
        # Para cada ponto acima de 25 no IMC, reduza as calorias
        calorias_reduzidas = calorias_base - (imc - 25) * 200  # Ajuste esse fator conforme necessário
        return max(calorias_reduzidas, 1200)


ft.app(target=main)