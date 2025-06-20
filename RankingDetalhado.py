import flet as ft # Import a biblioteca Flet para criar do App
from DataBase import DataBase 


def RankingDetalhado(page: ft.Page) -> ft.Column | ft.Container:
    """Função que cria a tela de Ranking Detalhado do App."""
    Container_Ranking = ft.Ref[ft.Column]() # Cria uma referência para o Container de Ranking
    
    tournament = DataBase().get_DataBase('SELECT * FROM torneio;') # Obtém os dados do torneio do banco de dados
    
    
    Container_Ranking.current = ft.Container(
        content = ft.Column(
            controls = [
                tournament_Options := ft.Dropdown(
                    value = tournament.loc[0, 'id'],
                    label = 'Torneios: ',
                    hint_text = 'Selecione um torneio',
                    menu_height = 300,
                    color= ft.Colors.BLACK,
                    options = [
                        ft.dropdown.Option(key, name)
                        for key, name in tournament[['id', 'nome']].values.tolist()
                    ],
                    editable = True,
                    enable_filter = True
                )
            ],
            scroll = ft.ScrollMode.AUTO,
            expand = True
        ),
        expand = True
    )
    
    return Container_Ranking.current