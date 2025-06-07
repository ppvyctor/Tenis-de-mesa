import flet as ft
from .Signup import get_DataFrame
import sys

def Replace_Password(page: ft.Page, email: str) -> ft.Container:
    Container_Replace_Password = ft.Ref[ft.Container]()
    Confirmated_Change_Password = False
    
    
    def Validating_New_Password() -> None:
        nonlocal TextField_New_Password, TextField_Confirm_New_Password, Confirmated_Change_Password
        TextField_New_Password.error = False
        TextField_New_Password.error_text = ''
        
        TextField_Confirm_New_Password.error = False
        TextField_Confirm_New_Password.error_text = ''
        
        users = get_DataFrame("users")
        
        
        if TextField_New_Password.value == '' or TextField_Confirm_New_Password.value == '' :
            if TextField_New_Password.value == '':
                TextField_New_Password.error = True
                TextField_New_Password.error_text = "* Campo obrigatório"
                
            if TextField_Confirm_New_Password.value == '':
                TextField_Confirm_New_Password.error = True
                TextField_Confirm_New_Password.error_text = "* Campo obrigatório"
        
        else:
            if TextField_New_Password.value != TextField_Confirm_New_Password.value:
                TextField_New_Password.error = True
                TextField_New_Password.error_text = "* Senhas não coincidem"
                
                TextField_Confirm_New_Password.error = True
                TextField_Confirm_New_Password.error_text = "* Senhas não coincidem"
            
            elif users[users["Email"] == email]["Password"].values[0] == TextField_New_Password.value:
                TextField_New_Password.error = True
                TextField_New_Password.error_text = "* Senha igual a já casdastrada"
                
                TextField_Confirm_New_Password.error = True
                TextField_Confirm_New_Password.error_text = "* Senha igual a já cadastrada"
            
            else:
                Confirmated_Change_Password = True
                
                users.loc[users["Email"] == email, "Password"] = TextField_New_Password.value
                
                if "\\" in sys.path[0]:
                    path = sys.path[0] + f'\\Users\\users.xlsx'
                
                else:
                    path = sys.path[0] + f'/Users/users.xlsx'
                    
                users.to_excel(path, index=False)
                
                update_layout()
                
        
        page.update()
            
    
    
    def update_layout() -> None:
        nonlocal Container_Replace_Password, TextField_New_Password, TextField_Confirm_New_Password
        
        
        if Confirmated_Change_Password:
            Container_Replace_Password.current.content = ft.Row(
                controls = [
                    ft.Icon(
                        name = ft.Icons.CHECK,
                        color = ft.Colors.GREEN,
                        size = 24,
                    ),
                    
                    ft.Text(
                        "Senha alterada com sucesso!\nVolte a tela de login.",
                        color = ft.Colors.GREEN,
                        size = 20,
                        weight = 'bold'
                    )
                ]
            )
        
        else:
            Container_Replace_Password.current.content = ft.Column(
                controls=[
                    ft.Text(
                        "Alterar senha",
                        size = 20,
                        color = ft.Colors.BLACK,
                        weight = 'bold'
                    ),
                    
                    TextField_New_Password := ft.TextField(
                        label = "Nova senha: ",
                        hint_text = "Digite sua nova senha",
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
                        )
                    ),
                        
                    TextField_Confirm_New_Password := ft.TextField(
                        label = "Confirme sua nova senha: ",
                        hint_text = "Digite sua nova senha",
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
                        on_blur = lambda e: Validating_New_Password()
                    ),
                    
                    Button_Replace_Password := ft.ElevatedButton(
                        content = ft.Text("Alterar senha", color = ft.Colors.WHITE),
                        bgcolor = ft.Colors.BLUE,
                        width = 320,
                        height = 40,
                        on_click = lambda e: Validating_New_Password()
                    )
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            )
        
        page.update()
    
    
    Container_Replace_Password.current = ft.Container(
        content = ft.Column(
            controls=[
                ft.Text(
                    "Alterar senha",
                    size = 20,
                    color = ft.Colors.BLACK,
                    weight = 'bold'
                ),
                
                TextField_New_Password := ft.TextField(
                    label = "Nova senha: ",
                    hint_text = "Digite sua nova senha",
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
                    )
                ),
                    
                TextField_Confirm_New_Password := ft.TextField(
                    label = "Confirme sua nova senha: ",
                    hint_text = "Digite sua nova senha",
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
                    )
                ),
                
                Button_Replace_Password := ft.ElevatedButton(
                    content = ft.Text("Alterar senha", color = ft.Colors.WHITE),
                    bgcolor = ft.Colors.BLUE,
                    width = 320,
                    height = 40
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        
        bgcolor = ft.Colors.WHITE,
        width = 320,
        height = 200
    )
    
    update_layout()
    
    return Container_Replace_Password.current