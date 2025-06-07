import flet as ft
import re
from .Login import get_DataFrame
from .Send_Email import Send_Email

def ForgetPassword(page: ft.Page) -> ft.Container:
    Screen_Send_Email = False
    Container_Forget_Password = ft.Ref[ft.Container]()
    
    
    def Validating_Email() -> None:
        nonlocal Screen_Send_Email
    
        TextField_Email.value = TextField_Email.value.lower()
        
        TextField_Email.error = False
        TextField_Email.error_text = ""
        Container_Forget_Password.current.height = 160
        
        if TextField_Email.value == "":
            TextField_Email.error = True
            TextField_Email.error_text = "* Campo obrigatório"
            Container_Forget_Password.current.height += 20
        
            
        elif re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", TextField_Email.value) is None:
            TextField_Email.error = True
            TextField_Email.error_text = "* Email inválido"
            Container_Forget_Password.current.height += 20
        
            
        elif TextField_Email.value not in get_DataFrame("users")["Email"].values:
            TextField_Email.error = True
            TextField_Email.error_text = "* Email não cadastrado"
            Container_Forget_Password.current.height += 20
            
        
        else:
            Screen_Send_Email = True
            update_layout()
    
        page.update()
    
    def update_layout() -> None:
        if Screen_Send_Email:
            
            Container_Forget_Password.current.height += 110
            
            if len(TextField_Email.value) >= 36: Container_Forget_Password.current.height += 20
            
            elif len(TextField_Email.value) == 42: Container_Forget_Password.current.height += 20
            
            if len(TextField_Email.value) > 76: Container_Forget_Password.current.height += 20
            
            Container_Forget_Password.current.content = ft.Row(
                controls = [
                    ft.Text(value = "Enviando código de\nrecuperação de senha\nPor favor, aguarde...", color = ft.Colors.BLACK, size = 20, weight = 'bold'),
                    
                    ft.Icon(name = ft.Icons.HOURGLASS_EMPTY)
                ],
                width = 320,
                height = 160,
                adaptive = ft.alignment.center
            )
            
            page.update()
            
            Container_Forget_Password.current.content = Send_Email(page, TextField_Email.value.lower())
            
        else:
            Container_Forget_Password.current.content = ft.Column(
                controls = [
                    ft.Text(
                        value = "Recuperação de senha",
                        color = ft.Colors.BLACK,
                        size = 20,
                        weight = 'bold'
                    ),
                    
                    TextField_Email,
                    Button_Send_Email
                ],
                
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
                
            )
            
        page.update()
    

    Container_Forget_Password.current = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    value = "Recuperação de senha",
                    color = ft.Colors.BLACK,
                    size = 20,
                    weight = 'bold'
                ),
                
                TextField_Email := ft.TextField(
                    label = "Email",
                    max_length = 100,
                    hint_text = "Digite seu email",
                    color = ft.Colors.BLACK,
                    icon = ft.Icons.EMAIL,
                    keyboard_type = ft.KeyboardType.EMAIL,
                    autofill_hints = ft.AutofillHint.EMAIL,
                    border = ft.InputBorder.UNDERLINE,
                    input_filter = ft.InputFilter(
                        regex_string = r"^[a-zA-Z0-9.!@#$%&'*+-/=?^_{|}~]*$",
                        allow = False
                    )
                ),
                
                Button_Send_Email := ft.FloatingActionButton(
                    content = ft.Text("Continuar", color = ft.Colors.WHITE),
                    bgcolor = ft.Colors.BLUE,
                    width = 320,
                    height = 40,
                    on_click = lambda e: Validating_Email()
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        width = 320,
        height = 160,
        bgcolor = ft.Colors.WHITE,
        border_radius = 10,
        padding = ft.padding.only(top=10, left=8, right=8)
    )
    
    
    update_layout()

    return Container_Forget_Password.current