import pandas as pd # Importando a biblioteca pandas para manipulação de dados
from datetime import datetime # Importando a classe datetime para manipulação de datas e horas
import psycopg2

class Ranking: # Classe para manipulação do ranking
    def __init__(self): # Método construtor da classe
        host = "dpg-d0if6jodl3ps73cjqnng-a.oregon-postgres.render.com"  # Endereço do servidor, pode ser um IP ou 'localhost' para o servidor local
        port = "5432"       # Porta padrão do PostgreSQL
        dbname = "pingpong_grjk" # Nome do banco de dados
        user = "pingpong_grjk_user" # Nome de usuário do banco de dados
        password = "zwwUd1vJIY9W7pQZ9hasoxbDuZzB4h5I" # Senha do usuário do banco de dados
        
        try:
            # Tentativa de conexão com o banco de dados PostgreSQL
            self.conn = psycopg2.connect(
                host=host, # Endereço do servidor
                port=port, # Porta do servidor
                dbname=dbname, # Nome do banco de dados
                user=user, # Nome de usuário do banco de dados
                password=password # Senha do usuário do banco de dados
            )
                
            self.conection = True # Atributo para verificar se a conexão foi bem-sucedida
            
        except:
            self.conection = False # Atributo para verificar se a conexão foi bem-sucedida
            
    def verify_connection(self):
        """Verifica se a conexão com o banco de dados foi bem-sucedida."""
        return self.conection
    
    def close(self):
        if self.connected:
            self.conn.close()
            self.connected = False
            
    
    def insert_Player(self, first_name: str, last_name: str, bird_date: datetime, style: str,
                      id_time: int, id_pais: int, sex: str, password: str):
        '''Insere um novo jogador no banco de dados.'''
        
        cursor = self.conn.cursor() # Cria um cursor para executar comandos SQL
        command = '''INSERT INT atleta (nome, sobrenome, data nascimento, estilo, id_time, id_pais, sexo, senha)'''