from DataBase import DataBase
from tqdm import tqdm
database = DataBase()
matchs = database.get_DataBase('select * from partida where fase = \'Final\' order by id asc;')
matchs

count = 0
num = 1
for key in tqdm(matchs['id']):
    database.update_Player(
        f'update partida set contador_partida = {num} where id = {key};'
    )
    
    if count == 1:
        count = 0
        num += 1
    
    else:
        count += 1