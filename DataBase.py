import pandas as pd # Importando a biblioteca pandas para manipulação de dados
from sqlalchemy import create_engine

class DataBase: # Classe para manipulação do DataBase
    def __init__(self) -> None: # Método construtor da classe
        host = "dpg-d0if6jodl3ps73cjqnng-a.oregon-postgres.render.com"  # Endereço do servidor, pode ser um IP ou 'localhost' para o servidor local
        port = "5432"       # Porta padrão do PostgreSQL
        dbname = "pingpong_grjk" # Nome do banco de dados
        user = "pingpong_grjk_user" # Nome de usuário do banco de dados
        password = "zwwUd1vJIY9W7pQZ9hasoxbDuZzB4h5I" # Senha do usuário do banco de dados

        try:
            self.engine = create_engine(
                f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
            )
            self.conection = True
        except:
            self.conection = False


    def verify_connection(self) -> bool:
        """Verifica se a conexão com o banco de dados foi bem-sucedida."""
        return self.conection


    def close(self) -> None:
        '''Fecha a conexão com o banco de dados se estiver conectada.'''
        
        if self.conection:
            
            self.engine.dispose()
            self.conection = False
            
    
    def insert_Player(self, tabela_Name: str, Columns: str, datas: tuple) -> None:
        '''Insere um novo jogador no banco de dados.'''

        placeholders = ', '.join(['%s'] * len(datas))
        command = f"INSERT INTO {tabela_Name} {Columns} VALUES ({placeholders})"
        
        conn = self.engine.raw_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(command, datas)
            finally:
                cursor.close()
            conn.commit()
        finally:
            conn.close()
    
    

    def get_DataBase(self, Command: str) -> pd.DataFrame:
        return pd.read_sql(Command, self.engine)