import flet as ft # Importando a biblioteca Flet
from .Login import Login # Importando a classe Login
from .ForgetPassword import ForgetPassword # Importando a classe ForgetPassword
from .Signup import signUp # Importando a classe signUp


def mainLogin(page: ft.Page) -> ft.Container:
    Container_mainLogin = ft.Ref[ft.Container]() # Container principal da tela de login
    
    Login_Screen = True # Declarando variável que controla a tela de login
    Forget_Password_Screen = False # Declaração de variável que controla a tela de esqueceu a senha
    Register_Screen = False # Declaração de variável que controla a tela de cadastro
            
        
    def update_layout() -> None: # Função que atualiza o layout da tela de login
        nonlocal Container_mainLogin # Declarando que a variável Container_mainLogin é global
        
        if Login_Screen: # Se a tela de login estiver ativa
            Container_mainLogin.current.content = ft.Container( # Container principal da tela de login
                ft.Column(
                    controls = [
                        Container_Mensage,
                        
                        ft.Container(
                            width = 320,
                            height = 5
                        ),
                        
                        Container_Login,
                        
                        ft.Container(
                            content = ft.Divider(
                                color = ft.Colors.ON_SURFACE_VARIANT,
                                height = 100
                            ),
                            width = 320
                        ),
                        
                        singupButton
                    ],
                    spacing = 1,
                    expand = True,
                    alignment = ft.MainAxisAlignment.CENTER,
                ),
                expand = True,
                alignment = ft.alignment.center
            )
        
        elif Forget_Password_Screen:
            Container_mainLogin.current.content = ft.Container(
                content = ft.Column(
                        controls = [
                            ft.Row(
                                controls = [
                                    ft.IconButton(
                                        icon = ft.Icons.ARROW_BACK,
                                        icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                        icon_size = 30,
                                        tooltip = "Voltar para a tela de login",
                                        on_click = lambda e: change_To_Login()
                                    ),
                                    
                                    ft.Text(
                                        "Voltar a tela de login",
                                        weight = 'bold',
                                        size = 20,
                                        color = ft.Colors.ON_SURFACE_VARIANT
                                    )
                                ],
                                
                                alignment = ft.MainAxisAlignment.CENTER
                            ),
                            
                            ft.Container(  # Adicionando um Container para centralizar ForgetPassword
                                content = ForgetPassword(page),
                                alignment = ft.alignment.center,  # Centraliza o Container na tela
                                height = 600
                            )
                        ],
                        height = 600,
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER
                    ),
                
                    expand = True
                )  
            
            
        
        else:
            Container_mainLogin.current.content = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Row(
                            controls = [
                                ft.IconButton(
                                    icon = ft.Icons.ARROW_BACK,
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                    icon_size = 30,
                                    tooltip = "Voltar para a tela de login",
                                    on_click = lambda e: change_To_Login()
                                ),
                                
                                ft.Text(
                                    "Voltar a tela de login",
                                    weight = 'bold',
                                    size = 20,
                                    color = ft.Colors.ON_SURFACE_VARIANT
                                )
                            ],
                            
                            alignment = ft.MainAxisAlignment.CENTER
                        ),
                        
                        ft.Container(
                            content = signUp(page),
                            alignment = ft.alignment.center,  # Centraliza o Container na tela
                            height = 600
                        )
                    ],
                    expand = True,
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                ),
                
                expand = True
            )
            
            
        page.update()


    def change_To_Login() -> None:
        nonlocal Login_Screen, Forget_Password_Screen, Register_Screen
        
        Login_Screen = True
        Forget_Password_Screen = False
        Register_Screen = False
        
        update_layout()
    
    
    def change_To_Forget_Password_Screen() -> None:
        nonlocal Login_Screen, Forget_Password_Screen, Register_Screen
        
        Login_Screen = False
        Forget_Password_Screen = True
        Register_Screen = False
        
        update_layout()
            
            
    def change_To_SignUp() -> None:
        nonlocal Login_Screen, Forget_Password_Screen, Register_Screen
        
        Login_Screen = False
        Forget_Password_Screen = False
        Register_Screen = True
        
        update_layout()
            

    Container_Mensage = ft.Container(
        content = ft.Row(
            controls = [
                Icon_Mensage := ft.Icon(),
                TextField_Mensage := ft.Text()
            ]
        ),
        
        width = 320,
        height = 40,
        bgcolor = ft.Colors.TRANSPARENT,
        border_radius = 10,
        padding = ft.padding.only(top = 10, left = 8, right = 8),
        alignment = ft.alignment.top_center
    )


    Container_Login = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    value = "Login",
                    color = ft.Colors.BLACK,
                    size = 20,
                    weight = 'bold'
                ),
                
                
                TextField_Email_or_Username := ft.TextField(
                    label = "Nome: ",
                    hint_text = "Digite seu Nome",
                    max_length = 100,
                    prefix_icon = ft.Icons.PERSON,
                    border = ft.InputBorder.UNDERLINE,
                    color = ft.Colors.BLACK,
                    keyboard_type = ft.KeyboardType.TEXT,
                    input_filter = ft.InputFilter(
                        regex_string = r"^[a-zA-Z0-9\u00C0-\u00FF_ \-]*$",
                        allow = False
                    )
                ),
                
                
                TextField_Password := ft.TextField(
                    label = "Senha: ",
                    hint_text = "Digite sua senha",
                    max_length = 100,
                    prefix_icon = ft.Icons.KEY,
                    color = ft.Colors.BLACK,
                    password = True,
                    can_reveal_password = True,
                    border = ft.InputBorder.UNDERLINE,
                    input_filter = ft.InputFilter(
                        regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$',
                        allow = False
                    ),
                    keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD,
                    on_blur = lambda e: Login(page, Container_Mensage, Container_Login,
                                               TextField_Mensage, TextField_Email_or_Username, TextField_Password,
                                               Icon_Mensage)
                ),
                
                
                ft.FloatingActionButton(
                    content = ft.Text("Login", color = ft.Colors.WHITE),
                    bgcolor = ft.Colors.BLUE,
                    width = 320,
                    height = 40,
                    on_click = lambda e: Login(page, Container_Mensage, Container_Login,
                                               TextField_Mensage, TextField_Email_or_Username, TextField_Password,
                                               Icon_Mensage)
                ),
                
                
                ft.TextButton(
                    text = 'Esqueceu a senha?',
                    width = 320,
                    style = ft.ButtonStyle(
                        color = ft.Colors.BLUE
                    ),
                    on_click = lambda e: change_To_Forget_Password_Screen()
                )
                
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            expand = True
        ),
        width = 320,
        height = 260,
        bgcolor = ft.Colors.WHITE,
        border_radius = 10,
        padding = ft.padding.only(top = 10, left = 8, right = 8)
    )
    
    
    singupButton = ft.FloatingActionButton(
        content = ft.Text("Criar nova conta", color = ft.Colors.WHITE),
        bgcolor = ft.Colors.GREEN,
        width = 320,
        height = 40,
        on_click = lambda e: change_To_SignUp()
    )


    Container_mainLogin.current = ft.Container(
        ft.Column(
            controls = [
                Container_Mensage,
                
                ft.Container(
                    width = 320,
                    height = 5
                ),
                
                Container_Login,
                
                ft.Container(
                    content = ft.Divider(
                        color = ft.Colors.ON_SURFACE_VARIANT,
                        height = 100
                    ),
                    width = 320
                ),
                
                singupButton
            ],
            spacing = 1,
            expand = True,
            alignment = ft.MainAxisAlignment.CENTER,
        ),
        expand = True,
        alignment = ft.alignment.center
    )
    

    update_layout()

    return Container_mainLogin.current