import flet as ft
import random
import smtplib
import email.message as em
import pandas as pd
import sys
from .Login import get_DataFrame
from .ReplacePassword import Replace_Password


def Send_Code(email: str) -> bool | str:
    try:
        credentials = {
            "email": 'pingpong.pucsp@gmail.com',
            "appkey": 'wyqp aemw xhke ispn'
        }
        
        code = random.randint(100000, 999999)
        
        corpo = """
            <!DOCTYPE html>
            <html lang="pt-BR">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }
                    .email-container {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    .email-header {
                        text-align: center;
                        padding-bottom: 20px;
                        border-bottom: 1px solid #dddddd;
                    }
                    .email-body {
                        padding: 20px;
                        text-align: center;
                    }
                    .email-body h1 {
                        color: #333333;
                    }
                    .email-body p {
                        color: #666666;
                        line-height: 1.6;
                    }
                    .confirmation-code {
                        display: inline-block;
                        padding: 10px 20px;
                        margin-top: 20px;
                        background-color: #4CAF50;
                        color: #ffffff;
                        border-radius: 5px;
                        font-size: 18px;
                        font-weight: bold;
                    }
                    .email-footer {
                        text-align: center;
                        padding-top: 20px;
                        border-top: 1px solid #dddddd;
                        color: #aaaaaa;
                        font-size: 12px;
                    }
                    .email-footer a {
                        color: #4CAF50;
                        text-decoration: none;
                    }
                </style>""" + f"""
            </head>
            <body>
                <div class="email-container">
                    <div class="email-header"></div>
                    <div class="email-body">
                        <h1>Recuperação de Senha</h1>
                        <p>Olá,</p>
                        <p>Recebemos uma solicitação para redefinir sua senha. Use o código de confirmação abaixo para continuar com o processo de recuperação de senha.</p>
                        <div class="confirmation-code">{code}</div>
                        <p>Se você não solicitou a recuperação de senha, por favor, ignore este e-mail.</p>
                    </div>
                </div>
            </body>
            </html>
        """ 
        msg = em.Message()
        msg['Subject'] = 'Recuperar Senha - Ping Pong'.upper()
        msg['From'] = credentials['email']
        msg['To'] = email
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo)
        
        smtp = smtplib.SMTP('smtp.gmail.com: 587')
        smtp.starttls()
        smtp.login(msg['From'], credentials['appkey'])
        smtp.sendmail(
            msg['From'],
            [msg['To']],
            msg.as_string().encode('UTF-8')
        )

        return str(code)
    except:
        return False
        

def Send_Email(page: ft.Page, email: str, isSignUp = False, database = None) -> ft.Container:
    Screen_Replace_Password = False
    Container_Send_Email = ft.Ref[ft.Container]()
    
    
    def Validation_Code(code: str) -> None:
        nonlocal Screen_Replace_Password
        
        TextField_Code.error = False
        TextField_Code.error_text = ''
        
        if TextField_Code.value == '':
            TextField_Code.error = True
            TextField_Code.error_text = '* Campo obrigatório'
        
        elif len(TextField_Code.value) < 6:
            TextField_Code.error = True
            TextField_Code.error_text = "* O código deve conter 6 dígitos"
        
        elif TextField_Code.value != code:
            TextField_Code.error = True
            TextField_Code.error_text = "* Código inválido"
            
        else:
            Screen_Replace_Password = True
            update_layout()
        
        page.update()
        
    
    def resend_code() -> None:
        nonlocal send_code, Container_Send_Email
        
        Container_Send_Email.current.content.controls[1].value = "Código de recuperação reenviado para o email: " + email
        page.update()
        send_code = Send_Code(email)
        page.update()
        
    
    
    def update_layout() -> None:
        nonlocal Container_Send_Email, Screen_Replace_Password, send_code, TextField_Code, Button_Code, Button_Forget_Password
        
        if Screen_Replace_Password:
            
            if isSignUp:
                if "\\" in sys.path[0]:
                    path = sys.path[0] + f'\\Users\\users.xlsx'
                
                else:
                    path = sys.path[0] + f'/Users/users.xlsx' 
                
                pd.concat(
                    [
                        get_DataFrame("users"),
                        database
                    ],
                    
                    ignore_index = True
                ).to_excel(path, index = False)
                
                Container_Send_Email.current.width = 320
                Container_Send_Email.current.content = ft.Container(
                    content = ft.Row(
                        controls = [
                            ft.Icon(
                                name = ft.Icons.CHECK,
                                color = ft.Colors.GREEN,
                            ),
                            
                            ft.Text(
                                value = "Cadastro realizado com\nsucesso!🎉Volte ao login\npara acessar sua conta",
                                color = ft.Colors.GREEN,
                                size = 20,
                                weight = 'bold'
                            )
                        ],
                        height = ft.CrossAxisAlignment.CENTER
                    )
                )
            
            else:
                Container_Send_Email.current.content = Replace_Password(page, email)
        
        else:
            if send_code is not False:
                Container_Send_Email.current.content = ft.Column(
                    controls = [
                        ft.Text(
                            value = "Recuperação de senha",
                            color = ft.Colors.BLACK,
                            size = 20,
                            weight = 'bold'
                        ),
                        
                        ft.Text(
                            "Enviamos um código de recuperação para o email: " + email,
                            color = ft.Colors.BLACK,
                            size = 14
                        ),
                        
                        TextField_Code := ft.TextField(
                            label = "Digite o código enviado por email:",
                            hint_text = "Código de recuperação",
                            color = ft.Colors.BLACK,
                            icon = ft.Icons.LOCK,
                            keyboard_type = ft.KeyboardType.NUMBER,
                            border = ft.InputBorder.UNDERLINE,
                            input_filter = ft.InputFilter(
                                regex_string = r'^[0-9]*$',
                                allow = False
                            ),
                            max_length = 6,
                            on_blur = lambda e: Validation_Code(send_code)
                        ),
                        
                        Button_Code := ft.ElevatedButton(
                            content = ft.Text("Enviar Código", color = ft.Colors.WHITE),
                            bgcolor = ft.Colors.BLUE,
                            width = 320,
                            height = 40,
                            on_click = lambda e: Validation_Code(send_code)
                        ),
                        
                        Button_Forget_Password := ft.TextButton(
                            text = 'Reenviar código',
                            width = 320,
                            style = ft.ButtonStyle(
                                color = ft.Colors.BLUE
                            ),
                            on_click = lambda e: resend_code()
                        )
                    ],
                    
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                )
            
            else:
                Container_Send_Email.current.content = ft.Row(
                    controls = [
                        ft.Icon(
                            name = ft.Icons.ERROR,
                            color = ft.Colors.RED_400,
                        ),
                        
                        ft.Text(
                            value = "Desculpe, no momento não\nfoi possível enviar o código\nde recuperação. 😔",
                            color = ft.Colors.RED_400,
                            size = 20,
                            weight = 'bold'
                        )
                    ]
                )
            
        page.update()
    
    send_code = Send_Code(email)
    
    Container_Send_Email.current = ft.Container(
        content = ft.Column(
            controls = [
                ft.Text(
                    "Recuperação de senha",
                    color = ft.Colors.BLACK,
                    weight = 'bold',
                    size = 20
                ),
                
                ft.Text(
                    "Enviamos um código de recuperação para o email: " + email,
                    color = ft.Colors.BLACK,
                    size = 14
                ),
                
                TextField_Code := ft.TextField(
                    label = "Digite o código enviado por email:",
                    hint_text = "Código de recuperação",
                    color = ft.Colors.BLACK,
                    icon = ft.Icons.LOCK,
                    keyboard_type = ft.KeyboardType.NUMBER,
                    border = ft.InputBorder.UNDERLINE,
                    input_filter = ft.InputFilter(
                        regex_string = r'^[0-9]*$',
                        allow = False
                    ),
                    max_length = 6
                ),
                
                Button_Code := ft.ElevatedButton(
                    content = ft.Text("Enviar Código", color = ft.Colors.WHITE),
                    bgcolor = ft.Colors.BLUE,
                    width = 320,
                    height = 40
                ),
                
                Button_Forget_Password := ft.TextButton(
                    text = 'Esqueceu a senha?',
                    width = 320,
                    style = ft.ButtonStyle(
                        color = ft.Colors.BLUE
                    )
                )
            ],
            alignment = ft.alignment.top_center,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        ),
        bgcolor = ft.Colors.WHITE,
        width = 320,
        height = 200
    )

    
    update_layout()
    
    
    return Container_Send_Email.current