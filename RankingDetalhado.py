import flet as ft # Import a biblioteca Flet para criar do App
import re
import regex # Import a biblioteca Regex para fazer expressões regulares
import numpy as np # Import a biblioteca pandas para manipulação de dados
from DataBase import DataBase 


def RankingDetalhado(page: ft.Page) -> ft.Column | ft.Container:
    '''# Configurações gerais do App
    page.title = 'Ranking Detalhado' # Definindo o título do App
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Centraliza o conteúdo verticalmente
    page.theme_mode = ft.ThemeMode.DARK # Definind tema escuro
    page.window.center() # Colocando a página no centro da tela'''
    
    
    if not DataBase().users.empty: # Se a base de dados não estiver vazia
        def search_Player(): # Função para pesquisar o jogador
            nonlocal up_Page # Dizendo que queremos modificar a variável up_Page que está fora da função
            up_Page.error = False
            up_Page.error_text = ''
            
            up_Page.value = up_Page.value.strip() # Remove os espaços em branco do início e do fim da string
            
            if up_Page.value != "": # Se o valor do TextField estiver vazio
                if re.sub(r'[ \-_0-9]', '', up_Page.value) == "":
                    up_Page.error = True
                    up_Page.error_text = "* Coloque um nome válido"
                    
                    page.update()
                
                else:
                    Creating_Ranking(up_Page.value.lower()) # Chama a função Creating_Ranking passando o valor do TextField como parâmetro
            
            else:
                Creating_Ranking()
            
        
        # Criando uma função para criar a tabela de ranking
        def Creating_Ranking(fill_player = None):
            '''Função que cria a tabela de ranking com as colunas Posição, Username, Wins, Defeats e Scores. Além de ordenar a base de dados de acordo com a coluna
            selecionada e o tipo de ordenação escolhida.'''
            
            nonlocal list_DataTable # Dizendo que queremos modificar a variável list_DataTable que está fora da função
            
            users = DataBase().users # Pega a base de dados dos usuários da classe Ranking
            
            '''Colocando os valores de derrota como negativo para que, em casos de empates, o jogador não se beneficie pela sua quantidade de derrotas.'''
            users["Defeats"] *= -1 
            users = users.sort_values(by = ["Scores", 'Wins', 'Defeats'], ascending = False) # Ordenando a base de dados de acordo com a coluna selecionada e o tipo de ordenação escolhida
            users["Defeats"] *= -1  # Voltando os valores de derrota para o valor original
            users.index = range(1, users.shape[0] + 1) # Definindo o índice da base de dados a partir de 1
            
            research = ""
            if fill_player is not None: # Se o valor do TextField não estiver vazio
                
                if len(fill_player) == 1:
                    research = f"({fill_player})" + "{e<=0}"
                
                elif len(fill_player) > 2:
                    research = f"({fill_player})" + "{e<=" + str(len(fill_player) // 3) + "}"

                else:
                    research = f"({fill_player})" + "{e<=1}"
                    
                users = users[users["Username"].isin(
                    [user for user in users["Username"] if regex.findall(research, user.lower()) != []] # Filtrando a base de dados de acordo com o valor do TextField
                )]
            
            # Limpa o ListView para adicionar a nova tabela de ranking
            list_DataTable.controls.clear()
            
            # Adiciona um DataTable ao ListView
            list_DataTable.controls.append(
                ft.DataTable( # Cria um DataTable para exibir os jogadores
                    columns = [ # Definindo as colunas do DataTable
                        ft.DataColumn(ft.Text('Posição')), # Definindo a coluna para exibir a posição dos jogadores
                        ft.DataColumn(ft.Text('Jogadores')), # Definindo a coluna para exibir os nomes dos jogadores
                        ft.DataColumn(ft.Text('Vitórias'), numeric = True), # Definindo a coluna para exibir as quantidades de vitórias dos jogadores
                        ft.DataColumn(ft.Text('Derrotas'), numeric = True), # Definindo a coluna para exibir as quantidades de derrotas dos jogadores
                        ft.DataColumn(ft.Text('Pontuação'), numeric = True) # Definindo a coluna para exibir as pontuações dos jogadores
                    ],
                    
                    rows = [ # Adicionando as linhas ao DataTable
                        ft.DataRow(cells = [ # Adiciona uma linha ao DataTable com as informações do jogador
                            ft.DataCell(ft.Text(str(index) + "º")), # Exibe a posição do jogador
                            ft.DataCell(ft.Text(row["Username"])), # Exibe o nome do jogador
                            ft.DataCell(ft.Text(str(row["Wins"]))), # Exibe a quantidade de vitórias do jogador
                            ft.DataCell(ft.Text(str(row["Defeats"]))),  # Exibe a quantidade de derrotas do jogador
                            ft.DataCell(ft.Text(str(row["Scores"]))) # Exibe a pontuação do jogador
                            ]
                        )
                    
                        for index, row in users.iterrows() # Loop para pegar cada linha do DataFrame users
                    ]
                )
            )
            
            page.update() # Atualiza a página
        
    
        # Criando um Container para adicionar o Text
        
        list_DataTable = ft.ListView(expand=True, spacing=10, padding=10) # Criando um ListView para exibir a tabela de ranking
        
        Creating_Ranking() # Chamando a função sort_DataBase_Ascending para ordenar a base de dados de acordo com o tipo de ordenação escolhida
        
        up_Page = ft.TextField(
            value = '',
            label = "Pesquisar jogador", # Definindo o texto do label
            hint_text = "Digite o nome do jogador", # Definindo o texto do hint
            color = ft.Colors.ON_SURFACE_VARIANT, # Definindo a cor do texto
            keyboard_type = ft.KeyboardType.TEXT,
            input_filter = ft.InputFilter(
                regex_string = r"^[a-zA-Z0-9\u00C0-\u00FF_ -]*$",
                allow = False
            ),
            on_click=lambda e: search_Player(), # Chamando a função search_Player ao clicar no TextField
            max_length = 25,
            autofocus = True, # Colocando o foco no TextField
            on_change = lambda e: search_Player() # Chamando a função Creating_Ranking ao pressionar Enter
        )
        
        down_Page = ft.Container( # Criando um Container para adicionar o ListView
            content = list_DataTable, # Adicionando o ListView ao Container
            expand = True # Expandindo o Container para preencher o espaço restante
        )
        
        
        
        return ft.Column(
            [ # Adicionando um Column para adicionar os Containers
             
                up_Page, # Adicionando o Container up_Page
                
                down_Page # Adicionando o Container down_Page
            ],
            expand = True # Expandindo o Column para preencher o espaço restante
        )

    else: # Caso a base de dados esteja vazia
        
        return ft.Container( # Criando um Container para adicionar o Text
            content = ft.Column(
                controls = [
                    ft.Text( # Adicionando o Text
                        "Nenhum jogador foi encontrado 😥", # Adicionando o texto
                        size = 30, # Definindo o tamanho do texto
                        weight = ft.FontWeight.BOLD, # Definindo o peso do texto
                    )
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Centralizando o texto
                alignment = ft.MainAxisAlignment.CENTER # Centralizando o texto
            ),
            expand = True, # Expandindo o Container para preencher o espaço restante
            alignment = ft.alignment.center # Centralizando o texto
        )
    
    
    '''OBS: Para o scroll do ListView funcionar, precisa-se delimitar corretamente o espaco onde o listView está inserido ou o espaço onde todos os containers,
    Columns ou Rows são inseridos.'''