import flet as ft
import pandas as pd
import sys
from datetime import datetime
import re


def get_DataFrame(databaseName: str) -> pd.DataFrame:
    if "\\" in sys.path[0]:
        path = sys.path[0] + f'\\Users\\{databaseName}.xlsx'
    
    else:
        path = sys.path[0] + f'/Users/{databaseName}.xlsx' 
    
    try:
        users = pd.read_excel(path) # Tentando Ler a base de dado dos usuários
        
    except FileNotFoundError: # Caso o arquivo não seja encontrado
        if databaseName == "users":
            users = pd.DataFrame(columns=['Username', 'Email', 'Password', 'Wins', 'Defeats', 'Scores']) # Cria um DataFrame vazio

        else:
            users = pd.DataFrame(columns=['Username', "Date", "Time"]) # Cria um DataFrame vazio
        
        users.to_excel(path, index=False) # Salva o DataFrame como um arquivo Excel
    
    return users


# Backend, e um pouco de frontend, do login
def Login(page: ft.Page,
          Container_Mensage: ft.Container, Container_Login: ft.Container,
          TextField_Mensage: ft.TextField, TextField_Email_or_Username: ft.TextField, TextField_Password: ft.TextField,
          Icon_Mensage: ft.Icon) -> None:
    
    
    users = get_DataFrame("users")
    
    # Ajustando o tamanho do container de login como padrão posto
    Container_Login.height = 260
    
    # Resetando os erros
    TextField_Email_or_Username.error = False,
    TextField_Email_or_Username.error_text = ''
    
    TextField_Password.error = False
    TextField_Password.error_text = ''
    
    Icon_Mensage.name = None
    
    TextField_Mensage.value = ''
    
    Container_Mensage.bgcolor = ft.Colors.TRANSPARENT
    
    page.update()
    
    if TextField_Email_or_Username.value == '' or TextField_Password.value == '':
        
        # Criando a mensagem de erro na barra de digitação
        if TextField_Email_or_Username.value == '':
            TextField_Email_or_Username.error = True,
            TextField_Email_or_Username.error_text = '* Campo obrigatório'
            Container_Login.height += 20
            
        
        if TextField_Password.value == '':
            TextField_Password.error = True
            TextField_Password.error_text = '* Campo obrigatório'
            Container_Login.height += 20
      
    elif '@' in TextField_Email_or_Username.value and re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", TextField_Email_or_Username.value) is None:
        TextField_Email_or_Username.error = True
        TextField_Email_or_Username.error_text = '* Email inválido'
        Container_Login.height += 20
      
    else:
        for index, row in users.iterrows():
            Icon_Mensage.name = ft.Icons.HOURGLASS_TOP
            Icon_Mensage.color = ft.Colors.BLUE
            
            TextField_Mensage.value = 'Buscando usuário... Aguarde!!'
            TextField_Mensage.color = ft.Colors.BLACK
            TextField_Mensage.size = 15
            TextField_Mensage.weight = 'bold'
            
            if (row["Username"] == TextField_Email_or_Username.value or row["Email"] == TextField_Email_or_Username.value.lower()) and row["Password"] == TextField_Password.value:
                
                users = get_DataFrame("usersTodayLoged")
                
                if not row["Username"] in users["Username"].values:
                    Icon_Mensage.name = ft.Icons.CHECK
                    Icon_Mensage.color = ft.Colors.BLUE
                    
                    TextField_Mensage.value = 'Login concluído, volte ao menu principal!'
                    TextField_Mensage.color = ft.Colors.BLACK
                    TextField_Mensage.size = 15
                    TextField_Mensage.weight = 'bold'
                    
                    Container_Mensage.bgcolor = ft.Colors.WHITE
                
                    
                
                    users = pd.concat([
                        users,
                        pd.DataFrame(
                            {
                                'Username': [row['Username']],
                                'Date': [datetime.now().strftime('%d/%m/%Y')],
                                'Time': [datetime.now().strftime('%H:%M:%S')]
                            }
                        )
                        ],
                        ignore_index = True
                    )
                    
                    if "\\" in sys.path[0]:
                        path = '\\'.join(sys.path[0].split("\\")) + f'\\Users\\usersTodayLoged.xlsx'
                    
                    else:
                        path = '/'.join(sys.path[0].split('/')) + '/Users/usersTodayLoged.xlsx' 
                    
                    users.to_excel(path, index = False)
                
                else:
                    Icon_Mensage.name = ft.Icons.CLOSE
                    Icon_Mensage.color = ft.Colors.RED_400
                    
                    TextField_Mensage.value = 'Usuário já está logado!!'
                    TextField_Mensage.color = ft.Colors.RED_400
                    TextField_Mensage.size = 15
                    TextField_Mensage.weight = 'bold'
                    
                    Container_Mensage.bgcolor = ft.Colors.WHITE
                    
                break

            
            if index == users.shape[0] - 1:
                Icon_Mensage.name = ft.Icons.ERROR
                Icon_Mensage.color = ft.Colors.RED_400
                
                TextField_Mensage.value = 'Usuário ou senha incorretos!!'
                TextField_Mensage.color = ft.Colors.RED_400
                TextField_Mensage.size = 15
                TextField_Mensage.weight = 'bold'
                
                Container_Mensage.bgcolor = ft.Colors.WHITE
        
    page.update()