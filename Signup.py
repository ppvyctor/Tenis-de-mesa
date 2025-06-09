import flet as ft
import pandas as pd
from DataBase import DataBase # Importando a classe DataBase para manipulação do DataBase
import os



def Signup(page: ft.Page, dataBase: DataBase) -> ft.Column:
    Accound_Confirmation = False
    Container_SignUp = ft.Ref[ft.Column]()
    
    
    def Accound_Verification() -> None:
        nonlocal Accound_Confirmation
        
        users = dataBase.get_DataBase("SELECT * FROM atleta") # Obtém o DataFrame com os usuários cadastrados
        
        TextField_Username.error = False
        TextField_Username.error_text = ""
        
        TextField_New_Password.error = False
        TextField_New_Password.error_text = ""
        
        TextField_Confirm_New_Password.error = False
        TextField_Confirm_New_Password.error_text = ""
        
        TextField_ADM_Code.error = False
        TextField_ADM_Code.error_text = ""
        
        Container_SignUp.current.height = 360
        Container_SignUp.current.controls[0].height = 360
        
        
        # Check if the username is valid
        if TextField_Username.value == '':
            TextField_Username.error = True
            TextField_Username.error_text = "* Campo obrigatório"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20
            
        elif TextField_Username.value.lower() in [user.lower() for user in users["Username"].values]:
            TextField_Username.error = True
            TextField_Username.error_text = "* Este nickname já está em uso."
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20


        # Check if the password is valid
        if TextField_New_Password.value == '':
            TextField_New_Password.error = True
            TextField_New_Password.error_text = "* Campo obrigatório"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20
            
        
        if TextField_Confirm_New_Password.value == '':
            TextField_Confirm_New_Password.error = True
            TextField_Confirm_New_Password.error_text = "* Campo obrigatório"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20
            
        
        if TextField_New_Password.value != TextField_Confirm_New_Password.value:
            TextField_New_Password.error = True
            TextField_New_Password.error_text = "* As senhas não coincidem"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20
            
            TextField_Confirm_New_Password.error = True
            TextField_Confirm_New_Password.error_text = "* As senhas não coincidem"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20
            
        
        # Check if the ADM code is valid
        if TextField_ADM_Code.value == '':
            TextField_ADM_Code.error = True
            TextField_ADM_Code.error_text = "* Campo obrigatório"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20 
        
        elif TextField_ADM_Code.value != 'Adm123':
            TextField_ADM_Code.error = True
            TextField_ADM_Code.error_text = "* Código inválido"
            Container_SignUp.current.height += 20
            Container_SignUp.current.controls[0].height += 20


        if not (((TextField_Username.error or TextField_New_Password.error) or TextField_Confirm_New_Password.error) or TextField_ADM_Code.error):
            Accound_Confirmation = True
            update_layout()
            
            
        page.update()
    
    
    def new_signup() -> None:
        nonlocal Accound_Confirmation
        
        Accound_Confirmation = False
        update_layout()
        
        page.update()
    
    
    def update_layout() -> None:
        nonlocal Container_SignUp, Accound_Confirmation, TextField_Confirm_New_Password
        
        if Accound_Confirmation:
            users = dataBase.get_DataBase("SELECT * FROM atleta") # Obtém o DataFrame com os usuários cadastrados
            
            users = pd.concat(
                [
                    users,
                    pd.DataFrame(
                        {
                            'Username': [TextField_Username.value],
                            'Password': [TextField_New_Password.value],
                            'Wins': [0],
                            'Defeats': [0],
                            'Scores': [0]
                        }
                    )
                ], ignore_index = True
            )
            users.to_excel(f'Users/users.xlsx', index = False) # Salva o DataFrame como um arquivo Excel
            
            Container_SignUp.current.controls.clear()
            Container_SignUp.current.controls.append(
                ft.Column(
                    controls = [
                        ft.Container(
                            content = ft.Column(
                                controls = [
                                    ft.Row(
                                        controls = [
                                            ft.Icon(
                                                name = ft.Icons.CHECK,
                                                color = ft.Colors.GREEN,
                                                weight = 'bold',
                                                size = 25
                                            ),
                                            
                                            ft.Text(
                                            "Cadastro realizado com sucesso!!",
                                                size = 25,
                                                weight = 'bold',
                                                color = ft.Colors.GREEN
                                            )
                                        ]
                                    ),
                                    
                                    ft.Text(
                                        '\n',
                                        size = 15
                                    ),
                                    
                                    ft.FloatingActionButton(
                                        content = ft.Text("Novo Cadastro", color = ft.Colors.WHITE, weight = 'bold', size = 20),
                                        bgcolor = ft.Colors.BLUE,
                                        width = 340,
                                        height = 40,
                                        autofocus = True,
                                        on_click = lambda e: new_signup()
                                    )
                                ],
                                alignment = ft.MainAxisAlignment.CENTER,
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER
                            ),
                            width = 450,
                            height = 240,
                            bgcolor = ft.Colors.WHITE,
                            border_radius = 10,
                            padding = ft.padding.only(top=10, left=8, right=8)
                        )
                    ],
                    expand = True,
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                )
            )
            
            TextField_Username.value = ''
            TextField_New_Password.value = ''
            TextField_Confirm_New_Password.value = ''
            TextField_ADM_Code.value = ''
            
            
        else:
            dataCountry = dataBase.get_DataBase("SELECT * FROM \"país\"") # Obtém o DataFrame com os países cadastrados
            Container_SignUp.current.controls.clear()
            Container_SignUp.current.controls.append(
                ft.Container(
                    content = ft.Column(
                        controls = [
                            ft.Text(
                                "Cadastro",
                                size = 25,
                                weight = 'bold',
                                color = ft.Colors.BLACK
                            ),
                            
                            ft.Row(
                                controls = [
                                    TextField_Username,
                                    country := ft.Dropdown(
                                        label = "País de Representação:",
                                        hint_text = "Selecione seu país",
                                        options = [
                                            ft.dropdown.Option(
                                                key = dataCountry.iloc[row, 0],
                                                text = dataCountry.iloc[row, 1],
                                            ) for row in range(dataCountry.shape[0])
                                        ],
                                        enable_search = True,
                                        editable = True,
                                        menu_height = 300
                                    )
                                ],
                                expand= True,
                            ),
                            TextField_New_Password,
                            TextField_Confirm_New_Password,
                            TextField_ADM_Code,
                            
                            ft.FloatingActionButton(
                                content = ft.Text("Cadastrar", color = ft.Colors.WHITE, weight = 'bold', size = 20),
                                bgcolor = ft.Colors.BLUE,
                                width = 340,
                                height = 40,
                                on_click = lambda e: Accound_Verification()
                            )
                        ],
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                    width = 340,
                    height = 360,
                    bgcolor = ft.Colors.WHITE,
                    border_radius = 10,
                    padding = ft.padding.only(top=10, left=8, right=8)
                )
            )
            
        page.update()
    
    
    def UsernameOn_Autofocus_Next():
        nonlocal TextField_New_Password
        TextField_New_Password.focus()
        page.update()
    
    
    def PasswordOn_Autofocus_Next():
        nonlocal TextField_Confirm_New_Password
        TextField_Confirm_New_Password.focus()
        page.update()
        
    def Confirm_PasswordOn_Autofocus_Next():
        nonlocal TextField_ADM_Code
        TextField_ADM_Code.focus()
        page.update()
    
    
    Container_SignUp.current = ft.Column(
        controls = [
            ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text(
                            "Cadastro",
                            size = 25,
                            weight = 'bold',
                            color = ft.Colors.BLACK
                        ),
                        
                        
                        TextField_Username := ft.TextField(
                            label = "Nickname: ",
                            hint_text = "Digite seu nickname",
                            max_length = 25,
                            prefix_icon = ft.Icons.PERSON,
                            border = ft.InputBorder.UNDERLINE,
                            color = ft.Colors.BLACK,
                            keyboard_type = ft.KeyboardType.TEXT,
                            input_filter = ft.InputFilter(
                                regex_string = r"^[a-zA-Z0-9._\u00C0-\u00FF]*$",
                                allow = False
                            ),
                            on_submit = lambda e: UsernameOn_Autofocus_Next(),
                            autofocus = True
                        ),


                        TextField_New_Password := ft.TextField(
                            label = "Senha: ",
                            hint_text = "Digite sua Senha",
                            max_length = 100,
                            prefix_icon = ft.Icons.LOCK,
                            keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD,
                            color = ft.Colors.BLACK,
                            password = True,
                            can_reveal_password = True,
                            border = ft.InputBorder.UNDERLINE,
                            input_filter = ft.InputFilter(
                                regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$',
                                allow = False
                            ),
                            on_submit = lambda e: PasswordOn_Autofocus_Next()
                        ),
                                
                        TextField_Confirm_New_Password := ft.TextField(
                            label = "Confirme sua senha: ",
                            hint_text = "Digite sua senha",
                            max_length = 100,
                            prefix_icon = ft.Icons.LOCK_OUTLINE,
                            keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD,
                            color = ft.Colors.BLACK,
                            password = True,
                            can_reveal_password = True,
                            border = ft.InputBorder.UNDERLINE,
                            input_filter = ft.InputFilter(
                                regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$',
                                allow = False
                            ),
                            on_submit = lambda e: Confirm_PasswordOn_Autofocus_Next()
                        ),
                        
                        TextField_ADM_Code := ft.TextField(
                            label = "Código do Administrador: ",
                            hint_text = "Digite a senha do Administrador",
                            max_length = 100,
                            prefix_icon = ft.Icons.KEY_OUTLINED,
                            keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD,
                            color = ft.Colors.BLACK,
                            password = True,
                            can_reveal_password = True,
                            border = ft.InputBorder.UNDERLINE,
                            input_filter = ft.InputFilter(
                                regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$',
                                allow = False
                            ),
                            on_submit = lambda e: Accound_Verification()
                        ),
                        
                        ft.FloatingActionButton(
                            content = ft.Text("Cadastrar", color = ft.Colors.WHITE, weight = 'bold', size = 20),
                            bgcolor = ft.Colors.BLUE,
                            width = 340,
                            height = 40,
                            on_click = lambda e: Accound_Verification()
                        )
                    ],
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                        
                
                width = 340,
                height = 360,
                bgcolor = ft.Colors.WHITE,
                border_radius = 10,
                padding = ft.padding.only(top=10, left=8, right=8)
            )
        ],
        expand = True,
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER
    )
    
    
    update_layout()
    
    return Container_SignUp.current