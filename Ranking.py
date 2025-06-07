import pandas as pd # Importando a biblioteca pandas para manipulação de dados
import os # Importando a biblioteca os para manipulação de arquivos e diretórios

class Ranking: # Classe para manipulação do ranking
    def __init__(self): # Método construtor da classe
        if not os.path.exists("Users"):
            os.makedirs("Users")
        
        try:
            self.users = pd.read_excel('Users/users.xlsx') # Tentando Ler a base de dado dos usuários
            
        except FileNotFoundError: # Caso o arquivo não seja encontrado
            self.users = pd.DataFrame(columns=['Username', 'Email', 'Password', 'Wins', 'Defeats', 'Scores']) # Cria um DataFrame vazio
            self.users.to_excel('Users/users.xlsx', index=False) # Salva o DataFrame como um arquivo Excel