import pandas as pd # Importa a biblioteca pandas para manipulação de dados
import flet as ft # Importa a biblioteca flet para criação do App
from DataBase import DataBase # Importa a classe Ranking do arquivo Ranking.py
from RankingDetalhado import RankingDetalhado # Importa a classe RankingDetalhado do arquivo RankingDetalhado.py
from Signup import Signup # Importa a função mainLogin do arquivo mainLogin.py
from Game import game # Importa a função game para contagem dos pontos
from datetime import datetime # Importa a classe datetime para manipulação de data e hora
import os # Importa a biblioteca os para manipulação de arquivos e diretórios

def main(page: ft.Page):
    # Configurações gerais do App
    page.title = 'Tênis de Mesa' # Define o título do App
    page.theme_mode = ft.ThemeMode.SYSTEM # Definindo tema escuro
    page.window.full_screen = True # Define o App para tela cheia
    page.window.icon = 'Icon/ping-pong.png' # Caminho do ícone do App


    page_Home = True # Variável para controlar a página inicial
    page_RankingDetalhado = False # Variável para controlar a página de ranking detalhado
    page_Game = False # Variável para controlar a página do jogo

    player_1_Code = True # Variável para controlar se o jogador 1 está definido e pronto para jogar
    player_2_Code = True # Variável para controlar se o jogador 2 está definido e pronto para jogar
    
    
    dataBase = DataBase() # Cria uma instância da classe DataBase para manipulação do banco de dados


    def change_Theme() -> None:
        '''Função para alternar entre os temas claro e escuro do App, dependendo do tema atual.'''
        
        if page.theme_mode == ft.ThemeMode.DARK: # Se o tema atual for escuro, muda para o tema claro
            page.theme_mode = ft.ThemeMode.LIGHT # Define o tema claro
        
        else: # Se o tema atual for claro, muda para o tema escuro
            page.theme_mode = ft.ThemeMode.DARK # 
            
        page.update()


    def go_To_Home() -> None:
        '''Função para voltar à página inicial do App'''
        
        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna. 
        Ela permite alterar o valor de variáveis de funções envolventes sem precisar passá-las como parâmetro.'''
        nonlocal page_RankingDetalhado, page_Home, page_Game 
        
        page_Game = False # Desativa a página do jogo
        page_Home = True # Ativa a página inicial
        page_RankingDetalhado = False # Desativa a página de ranking detalhado
        
        update_layout() # Chama a função update_layout para atualizar o layout da página


    def go_To_RankingDetalhado() -> None:
        '''Função para ir para a página de ranking detalhado do App'''
        
        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna. 
        Ela permite alterar o valor de variáveis de funções envolventes sem precisar passá-las como parâmetro.'''
        nonlocal page_RankingDetalhado, page_Home, page_Game
        
        page_Game = False # Desativa a página do jogo
        page_Home = False # Desativa a página inicial
        page_RankingDetalhado = True # Ativa a página de ranking detalhado
        update_layout() # Chama a função update_layout para atualizar o layout da página


    def go_To_Game() -> None:
        '''Função usada para reiniciar uma partida.'''
        
        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna. 
        Ela permite alterar o valor de variáveis de funções envolventes sem precisar passá-las como parâmetro.'''
        nonlocal page_Game, page_Home, page_RankingDetalhado
        
        page_Home = True # Ir para a página inicial da partida
        page_Game = True # ir para a partida com a configuração anterior
        page_RankingDetalhado = False # Desativa a página de ranking detalhado
        update_layout() # Chama a função update_layout para atualizar o layout da página


    def runSignup() -> None:
        '''Função usada para ir para a página de cadastro de jogadores.'''
         
        nonlocal page_RankingDetalhado, page_Home, page_Game
        
        page_Game = False # Desativa a página do jogo
        page_Home = False # Desativa a página inicial
        page_RankingDetalhado = False # Desativa a página de ranking detalhado
        
        # Com tudo acima desativado, o código irá automaticamente para a aba de cadastro de jogadores.
        update_layout() # Chama a função update_layout para atualizar o layout da página


    def confirme_Player_2(password: ft.TextField, alertDialog: ft.AlertDialog) -> None:
        '''Função usada para confirmar a senha do jogador 2. Isso serve como uma verificação de segurança para garantir que o jogador 2 é quem diz ser.'''
        
        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna. 
        Ela permite alterar o valor de variáveis de funções envolventes sem precisar passá-las como parâmetro.'''
        nonlocal player_2_Code, Player_2, users

        password.error = False # Reseta o erro do campo de senha
        password.error_text = "" # Reseta o texto de erro do campo de senha
        player_2_Code = False # Reseta o código do jogador 2 para falso, indicando que ele ainda não está definido corretamente


        # Verifica se o campo de senha está vazio
        if password.value == '':
            password.error = True # Ativar o designe de erro do campo de senha
            password.error_text = "Campo obrigatório" # Define o texto de erro do campo de senha

            player_2_Code = False # Define o código do jogador 2 como falso, indicando que ele ainda não está definido corretamente


        # Verifica se a senha digitada é igual à senha do jogador 2 no DataFrame users
        elif password.value != str(users.loc[users["Username"] == Player_2.value, "Password"].values[0]):
            password.error = True # Ativar o designe de erro do campo de senha
            password.error_text = "Senha incorreta" # Define o texto de erro do campo de senha
            Player_2.value = "Player 2" # Reseta o valor do campo de seleção do jogador 2 para "Player 2"

            player_2_Code = False# Define o código do jogador 2 como falso, indicando que ele ainda não está definido corretamente

        
        # Se a senha digitada for igual à senha do jogador 2 no DataFrame users e não for vazia
        else:
            player_2_Code = True # Define o código do jogador 2 como verdadeiro, indicando que ele está definido corretamente

            page.close(alertDialog) # Fecha o diálogo de confirmação de senha

            # Cria um novo diálogo de alerta para informar que a senha está correta
            alertDialog = ft.AlertDialog(
                title = ft.Text("Senha Correta!"),
                content = ft.Text("Jogador 2 Já está definido!"),
                actions = [
                    ft.TextButton("Fechar", on_click=lambda e: page.close(alertDialog))
                ]
            )
            
            page.open(alertDialog) # Abre o diálogo de alerta para informar que a senha está correta
        
        password.update() # Atualiza o campo de senha para refletir as mudanças feitas independente do que aconteceu
        
        
    def confirme_Player_1(password: ft.TextField, alertDialog: ft.AlertDialog) -> None:
        '''Função usada para confirmar a senha do jogador 1. Isso serve como uma verificação de segurança para garantir que o jogador 1 é quem diz ser.'''


        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna. 
        Ela permite alterar o valor de variáveis de funções envolventes sem precisar passá-las como parâmetro.'''
        nonlocal player_1_Code, Player_1, users

        password.error = False # Reseta o erro do campo de senha
        password.error_text = "" # Reseta o texto de erro do campo de senha
        player_1_Code = False # Reseta o código do jogador 1 para falso, indicando que ele ainda não está definido corretamente


        # Verifica se o campo de senha está vazio
        if password.value == '':
            password.error = True # Ativar o designe de erro do campo de senha
            password.error_text = "Campo obrigatório" # 
            
            player_1_Code = False # Define o código do jogador 1 como falso, indicando que ele ainda não está definido corretamente
        
        # Verifica se a senha digitada é igual à senha do jogador 1 no DataFrame users
        elif password.value != str(users.loc[users["Username"] == Player_1.value, "Password"].values[0]):
            password.error = True # Ativar o designe de erro do campo de senha
            password.error_text = "Senha incorreta" # Define o texto de erro do campo de senha
            Player_1.value = "Player 1" # Reseta o valor do campo de seleção do jogador 1 para "Player 1"
            
            player_1_Code = False # Define o código do jogador 1 como falso, indicando que ele ainda não está definido corretamente
        
        else:
            player_1_Code = True # Define o código do jogador 1 como verdadeiro, indicando que ele está definido corretamente
            
            page.close(alertDialog) # Fecha o diálogo de confirmação de senha
            
            # Cria um novo diálogo de alerta para informar que a senha está correta
            alertDialog = ft.AlertDialog(
                title = ft.Text("Senha Correta!"), # Define o título do diálogo de alerta
                content = ft.Text("Jogador 1 Já está definido!"), # Define o conteúdo do diálogo de alerta
                actions = [
                    ft.TextButton("Fechar", on_click=lambda e: page.close(alertDialog)) # Define o botão de ação do diálogo de alerta para fechar o diálogo
                ]
            )
            
            page.open(alertDialog) # Abre o diálogo de alerta para informar que a senha está correta
        
        password.update() # Atualiza o campo de senha para refletir as mudanças feitas independente do que aconteceu
    
    
    def change_player_1() -> None:
        '''Função usada para mudar o jogador 1. Esta função tira a opção de escolha do jogador escolhido na opção de escolha do player 2'''
        
        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna.'''
        nonlocal Player_1, Player_2, users, player_2_Code
        
        
        player_2_Code = False # Reseta o código do jogador 2 para falso, indicando que ele ainda não está definido corretamente
        
        # Verifica se o jogador 1 selecionado é diferente de "Player 1"
        if Player_2.value != "Player 2":
            # Cria um diálogo de alerta para solicitar a senha do jogador 2
            alertDialog = ft.AlertDialog(
                title = ft.Text("Digite a senha da conta!"), # Define o título do diálogo de alerta
                content = ft.Text("Digite a senha cadastrada ao criar sua conta no aplicativo. Caso tenha esquecido, entre em contato com o responsável pelo APP."), # Define o conteúdo do diálogo de alerta
                # Define as ações do diálogo de alerta, que incluem um campo de senha e um botão de confirmação
                actions = [
                    password := ft.TextField( # Cria um campo de senha
                        label = "Confirme sua senha: ", # Define o rótulo do campo de senha
                        hint_text = "Digite sua senha", # Define o texto de dica do campo de senha
                        max_length = 100, # Define o comprimento máximo do campo de senha
                        prefix_icon = ft.Icons.LOCK, # Define o ícone prefixo do campo de senha
                        keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD, # Define o tipo de teclado do campo de senha
                        color = ft.Colors.ON_SURFACE_VARIANT, # Define a cor do texto do campo de senha
                        password = True, # Define o campo como um campo de senha
                        can_reveal_password = True, # Permite revelar a senha digitada
                        width = 400, # Define a largura do campo de senha
                        border = ft.InputBorder.UNDERLINE, # Define a borda do campo de senha como sublinhado
                        input_filter = ft.InputFilter( # Define o filtro de entrada do campo de senha
                            regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$', # Define a expressão regular para filtrar a entrada
                            allow = False, # Define se a entrada é permitida ou não
                        ),
                        on_submit = lambda e: confirme_Player_2(password, alertDialog) # Define a ação a ser executada quando o usuário submeter o campo de senha
                    ),
                    
                    ft.FloatingActionButton( # Cria um botão flutuante para confirmar a senha
                        content = ft.Text("Confirmar Senha", color = ft.Colors.WHITE, weight = 'bold', size = 20), # Define o conteúdo do botão
                        bgcolor = ft.Colors.BLUE, # Define a cor de fundo do botão
                        width = 240, # Define a largura do botão
                        height = 40, # Define a altura do botão
                        on_click = lambda e: confirme_Player_2(password, alertDialog) # Define a ação a ser executada quando o botão for clicado
                    )
                ],
                actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN # Define o alinhamento das ações do diálogo de alerta
            )
            
            page.open(alertDialog) # Abre o diálogo de alerta para solicitar a senha do jogador 2
        
        # Se o jogador 1 selecionado for "Player 1", não é necessário solicitar a senha
        else:
            player_2_Code = True # Define o código do jogador 2 como verdadeiro, indicando que ele está definido corretamente
        
        # Atualiza as opções do jogador 2 para excluir o jogador 1 selecionado
        Player_1.options = [ft.dropdown.Option("Player 1")] + [ft.dropdown.Option(user) for user in users["Username"] if Player_2.value != user]
        page.update() # Atualiza a página para refletir as mudanças feitas
        
    
    def change_player_2() -> None:
        '''Função usada para mudar o jogador 2. Esta função tira a opção de escolha do jogador escolhido na opção de escolha do player 1'''
        
        # A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna.
        nonlocal Player_1, player_1_Code, Player_2, users
        
        
        player_1_Code = False # Reseta o código do jogador 1 para falso, indicando que ele ainda não está definido corretamente
        
        # Verifica se o jogador 1 selecionado é diferente de "Player 1"
        if Player_1.value != "Player 1":
            alertDialog = ft.AlertDialog(
                title = ft.Text("Digite a senha da conta!"), # Define o título do diálogo de alerta
                content = ft.Text("Digite a senha cadastrada ao criar sua conta no aplicativo. Caso tenha esquecido, entre em contato com o responsável pelo APP."), # Define o conteúdo do diálogo de alerta
                # Define as ações do diálogo de alerta, que incluem um campo de senha e um botão de confirmação
                actions = [
                    password := ft.TextField( # Cria um campo de senha
                        label = "Confirme sua senha: ", # Define o rótulo do campo de senha
                        hint_text = "Digite sua senha", # Define o texto de dica do campo de senha
                        max_length = 100, # Define o comprimento máximo do campo de senha
                        prefix_icon = ft.Icons.LOCK, # Define o ícone prefixo do campo de senha
                        keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD, # Define o tipo de teclado do campo de senha
                        color = ft.Colors.ON_SURFACE_VARIANT, # Define a cor do texto do campo de senha
                        password = True, # Define o campo como um campo de senha
                        can_reveal_password = True, # Permite revelar a senha digitada
                        width = 400, # Define a largura do campo de senha
                        border = ft.InputBorder.UNDERLINE, # Define a borda do campo de senha como sublinhado
                        input_filter = ft.InputFilter( # Define o filtro de entrada do campo de senha
                            regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$', # Define a expressão regular para filtrar a entrada
                            allow = False # Define se a entrada é permitida ou não
                        ),
                        on_submit = lambda e: confirme_Player_1(password, alertDialog) # Define a ação a ser executada quando o usuário submeter o campo de senha
                    ),

                    # Cria um botão flutuante para confirmar a senha
                    ft.FloatingActionButton(
                        content = ft.Text("Confirmar Senha", color = ft.Colors.WHITE, weight = 'bold', size = 20), # Define o conteúdo do botão
                        bgcolor = ft.Colors.BLUE, # Define a cor de fundo do botão
                        width = 240, # Define a largura do botão
                        height = 40, # Define a altura do botão
                        on_click = lambda e: confirme_Player_1(password, alertDialog) # Define a ação a ser executada quando o botão for clicado
                    )
                ],
                actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN # Define o alinhamento das ações do diálogo de alerta
            )
            page.open(alertDialog) # Abre o diálogo de alerta para solicitar a senha do jogador 1
        
        # Se o jogador 1 selecionado for "Player 1", não é necessário solicitar a senha
        else:
            player_1_Code = True # Define o código do jogador 1 como verdadeiro, indicando que ele está definido corretamente
        
        # Verifica se a opção de escolha do jogador 1 é diferente de da escolha do jogador Player 1
        Player_2.options = [ft.dropdown.Option("Player 2")] + [ft.dropdown.Option(user) for user in users["Username"] if Player_1.value != user]
        page.update() # Atualiza a página para refletir as mudanças feitas
    
    
    def update_layout() -> None:
        '''Função usada para atualizar o layout da página do App.'''
        
        '''A palavra-chave nonlocal é usada para indicar que uma variável definida em um escopo externo (mas não global) será modificada dentro de uma função interna. 
        Ela permite alterar o valor de variáveis de funções envolventes sem precisar passá-las como parâmetro.'''
        nonlocal users, Player_1, Player_2, page_Game
        
        page.clean() # Limpa a página antes de adicionar novos elementos
        
        # Verifica se a página inicial está ativa
        if page_Home:
            
            # Verifica se a página do jogo está ativa
            if page_Game:
                
                # Verifica se os jogadores estão definidos
                if not player_1_Code and not player_2_Code:
                    # Cria um diálogo de alerta para informar que ambos os jogadores não estão definidos
                    alert = ft.AlertDialog(
                        title = ft.Text("Jogadores não definidos!"), # Define o título do diálogo de alerta
                        content = ft.Text(f"Ambos jogadores devem ser definidos para continuar!"), # Define o conteúdo do diálogo de alerta
                        # Define as ações do diálogo de alerta, que incluem um botão de fechar
                        actions = [
                            ft.TextButton("Fechar", on_click=lambda e: page.close(alert)) # Define a ação do botão de fechar para fechar o diálogo
                        ]
                    )
                    
                    page_Game = False # Desativa a página do jogo
                    page.add(ft.Row(controls = [left_screen, right_screen], expand = True)) # Adiciona a tela esquerda e direita à página
                    
                    page.open(alert) # Abre o diálogo de alerta para informar que ambos os jogadores não estão definidos
                
                # Verifica se apenas o jogador 1 não está definido
                elif not player_1_Code:
                    # Cria um diálogo de alerta para informar que o jogador 1 não está defin
                    alert = ft.AlertDialog(
                        title = ft.Text("Jogador não definido!"), # Define o título do diálogo de alerta
                        content = ft.Text(f"Jogador 1 precisa ser definido para continuar!"), # Define o conteúdo do diálogo de alerta
                        actions = [ 
                            ft.TextButton("Fechar", on_click=lambda e: page.close(alert)) # Define a ação do botão de fechar para fechar o diálogo
                        ]
                    )
                    page_Game = False # Desativa a página do jogo
                    page.add(ft.Row(controls = [left_screen, right_screen], expand = True)) # Adiciona a tela esquerda e direita à página
                    
                    page.open(alert) # Abre o diálogo de alerta para informar que o jogador 1 não está definido
                
                # Verifica se apenas o jogador 2 não está definido
                elif not player_2_Code:
                    # Cria um diálogo de alerta para informar que o jogador 2 não está definido
                    alert = ft.AlertDialog(
                        title = ft.Text("Jogador não definido!"), # Define o título do diálogo de alerta
                        content = ft.Text(f"Jogador 2 precisa ser definido para continuar!"), # Define o conteúdo do diálogo de alerta
                        # Define as ações do diálogo de alerta, que incluem um botão de fechar
                        actions = [
                            ft.TextButton("Fechar", on_click=lambda e: page.close(alert)) # Define a ação do botão de fechar para fechar o diálogo
                        ]
                    )
                    page_Game = False # Desativa a página do jogo
                    page.add(ft.Row(controls = [left_screen, right_screen], expand = True)) # Adiciona a tela esquerda e direita à página
                    
                    page.open(alert) # Abre o diálogo de alerta para informar que o jogador 2 não está definido
                    
                # Se ambos os jogadores estão definidos corretamente
                else:
                    # Cria um diálogo de alerta para informar que ambos os jogadores estão
                    page.add(
                        ft.Row(
                            controls = [
                                left_screen, # Tela esquerda do App
                                
                                # Tela direita do App com o jogo
                                ft.Column(
                                    controls = [
                                        ft.Row(
                                            controls = [
                                                ft.IconButton( # Botão de iniciar o jogo
                                                    icon = ft.Icons.CLOSE, # Ícone do botão
                                                    tooltip = 'Encerrar partida', # Tooltip do botão
                                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão
                                                    icon_size = 60, # Tamanho do ícone do botão
                                                    on_click = lambda e: go_To_Home() # Ação do botão para voltar à página inicial
                                                ),
                                                
                                                
                                                # Botão de reiniciar a partida
                                                ft.IconButton( 
                                                    icon = ft.Icons.REFRESH, # Ícone do botão
                                                    tooltip = 'Reiniciar partida', # Tooltip do botão
                                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão
                                                    icon_size = 60, # Tamanho do ícone do botão
                                                    alignment = ft.alignment.center_right, # Alinhamento do botão
                                                    on_click = lambda e: go_To_Game() # Ação do botão para reiniciar a partida
                                                ),
                                            ],
                                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN # Alinhamento dos botões na linha
                                        ),
                                        
                                        game(page, Player_1.value, Player_2.value, Points_To_Win.value, Sets.value) # Chama a função game para iniciar o jogo com os jogadores selecionados e as configurações definidas
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal da coluna
                                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN, # Alinhamento vertical da coluna
                                    expand = True # Expande a coluna para ocupar todo o espaço disponível
                                )
                            ],
                            expand = True # Expande a linha para ocupar todo o espaço disponível
                        )
                    )
            
            # Verifica se a página do jogo não está ativa
            else:
                page.add(ft.Row(controls = [left_screen, right_screen], expand = True)) # Adiciona a tela esquerda e direita à página
                
                # Verifica se o diretório "Users" existe, caso contrário, cria o diretório
                if not os.path.exists("Users"): os.makedirs("Users")
                
                # Tenta ler o arquivo "Users/users.xlsx" e ordenar os usuários por nome de usuário
                try:
                    users = pd.read_excel("Users/users.xlsx").sort_values('Username', ascending = True).reset_index(drop = True) # Lê o arquivo Excel e ordena os usuários por nome de usuário
                
                # Se ocorrer um erro ao ler o arquivo, cria um DataFrame vazio e salva como "Users/users.xlsx"
                except:
                    users = pd.DataFrame(columns=["Username", 'Password', 'Wins', 'Defeats', 'Scores']) # Cria um DataFrame vazio com as colunas especificadas
                    users.to_excel("Users/users.xlsx", index = False) # Salva o DataFrame como "Users/users.xlsx"
                
                # Ordena os usuários por nome de usuário, ignorando a diferença entre maiúsculas e minúsculas
                users = users.sort_values('Username', ascending = True, key = lambda user: user.str.lower()).reset_index(drop = True)
                
                # Atualiza as opções dos jogadores 1 e 2 com os usuários disponíveis
                Player_1.options = [ft.dropdown.Option("Player 1")] + [ft.dropdown.Option(user) for user in users["Username"].values if Player_2.value != user]
                
                # Atualiza as opções do jogador 2 com os usuários disponíveis, excluindo o jogador 1 selecionado
                Player_2.options = [ft.dropdown.Option("Player 2")] + [ft.dropdown.Option(user) for user in users["Username"].values if Player_1.value != user]

        # Verifica se a página de ranking detalhado está ativa
        elif page_RankingDetalhado:
            page.add(ft.Row(controls = [left_screen, RankingDetalhado(page)], expand = True)) # Adiciona a tela esquerda e a página de ranking detalhado à página

        # Verifica se a página de cadastro de jogadores está ativa
        else:
            
            page.add(ft.Row(controls = [left_screen, Signup(page, dataBase)], expand = True)) # Adiciona a tela esquerda e a página de cadastro de jogadores à página
        
        page.update() # Atualiza a página para refletir as mudanças feitas


    if dataBase.verify_connection():
        # Conteúdo a esquerda do App
        left_screen = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Column(
                            controls = [
                                ft.IconButton(
                                    icon = ft.Icons.MENU, # Ícone do botão de menu
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão de menu
                                    icon_size = 45, # Tamanho do ícone do botão de menu
                                    height = 50, # Altura do botão de menu
                                    alignment = ft.alignment.center # Alinhamento do botão de menu
                                ),
                                
                                # Botão de ir para a página inicial
                                ft.IconButton(
                                    tooltip = "Página Inicial", # Tooltip do botão de página inicial
                                    icon = ft.Icons.SPORTS_ESPORTS, # Ícone do botão de página inicial
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão de página inicial
                                    icon_size = 35, # Tamanho do ícone do botão de página inicial
                                    height = 50, # Altura do botão de página inicial
                                    alignment = ft.alignment.center, # Alinhamento do botão de página inicial
                                    on_click = lambda e: go_To_Home() # Ação do botão para voltar à página inicial
                                ),
                                
                                # Botão de ir para a página de ranking detalhado
                                ft.IconButton(
                                    tooltip = "Cadastrar", # Tooltip do botão de cadastro
                                    icon = ft.Icons.PERSON_ADD, # Ícone do botão de cadastro
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão de cadastro
                                    icon_size = 35, # Tamanho do ícone do botão de cadastro
                                    height = 50, # Altura do botão de cadastro
                                    alignment = ft.alignment.center, # Alinhamento do botão de cadastro
                                    on_click = lambda e: runSignup() # Ação do botão para ir para a página de cadastro de jogadores
                                ),
                                
                                # Botão de remover jogador
                                ft.IconButton(
                                    tooltip = "Remover Jogador",
                                    icon = ft.Icons.PERSON_REMOVE,
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, 
                                    icon_size = 35,
                                    height = 50,
                                    alignment = ft.alignment.center
                                    #on_click = lambda e: runSignup()
                                ),

                                # Botão de ir para a página de ranking detalhado
                                ft.IconButton(
                                    tooltip = "Ranking Completo dos Jogadores", # Tooltip do botão de ranking
                                    icon = ft.Icons.EMOJI_EVENTS, # Ícone do botão de ranking
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão de ranking
                                    icon_size = 35, # Tamanho do ícone do botão de ranking
                                    on_click = lambda e: go_To_RankingDetalhado(), # Ação do botão para ir para a página de ranking detalhado
                                    height = 50, # Altura do botão de ranking
                                    alignment = ft.alignment.center # Alinhamento do botão de ranking
                                )
                            ]
                        ),
                        
                        ft.Column(
                            controls = [
                                # Botão de ir para a página de ranking geral
                                ft.IconButton(
                                    tooltip = "Mudar tema", # Tooltip do botão de mudança de tema
                                    icon = ft.Icons.BRIGHTNESS_6, # Ícone do botão de mudança de tema
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão de mudança de tema
                                    icon_size = 25, # Tamanho do ícone do botão de mudança de tema
                                    on_click = lambda e: change_Theme(), # Ação do botão para mudar o tema do App
                                    height = 50, # Altura do botão de mudança de tema
                                    alignment = ft.alignment.center # Alinhamento do botão de mudança de tema
                                ),
                                
                                # Botão de sair do App
                                ft.IconButton(
                                    tooltip = "Sair", # Tooltip do botão de sair
                                    icon = ft.Icons.EXIT_TO_APP, # Ícone do botão de sair
                                    icon_color = ft.Colors.ON_SURFACE_VARIANT, # Cor do ícone do botão de sair
                                    icon_size = 25, # Tamanho do ícone do botão de sair
                                    on_click = lambda e: page.window.close(), # Ação do botão para fechar o App
                                    height = 50, # Altura do botão de sair
                                    alignment = ft.alignment.center # Alinhamento do botão de sair
                                )
                            ]
                        )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN # Alinhamento dos controles na coluna
                ),
                width = 50 # Largura da tela esquerda do App
            )
        
        # Conteúdo a direita do App
        if not os.path.exists("Users"): os.makedirs("Users")
        
        try:
            users = pd.read_excel("Users/users.xlsx") # Tenta ler o arquivo Excel com os usuários
        
        except:
            users = pd.DataFrame(columns=["Username", "Password", "Wins", "Defeats", "Scores"]) # Se não conseguir ler o arquivo, cria um DataFrame vazio com as colunas especificadas
            users.to_excel("Users/users.xlsx", index = False) # Salva o DataFrame vazio como "Users/users.xlsx"
        
        users = users.sort_values('Username', ascending = True, key = lambda user: user.str.lower()).reset_index(drop = True) # Ordena os usuários pelo nome em ordem alfabética
        
        # Tela direita do App com os controles de seleção de jogadores e configurações da partida
        right_screen = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Row(
                        controls = [
                            ft.Column(
                                controls = [
                                    ft.Column(
                                        controls = [
                                            ft.Column(
                                                controls = [
                                                    ft.Text(
                                                        "Escolha o primeiro jogador abaixo:", # Texto de instrução para escolher o primeiro jogador
                                                        size = 15 # Tamanho do texto
                                                    ),
                                                    
                                                    # Dropdown para selecionar o primeiro jogador
                                                    Player_1 := ft.Dropdown(
                                                        value = "Player 1", # Valor inicial do dropdown
                                                        # Opções do dropdown, começando com "Player 1"
                                                        options = [ 
                                                            ft.dropdown.Option("Player 1")
                                                        ] + [ft.dropdown.Option(user) for user in users["Username"].values],
                                                        menu_height = 300, # Altura do menu do dropdown
                                                        color = ft.Colors.ON_SURFACE_VARIANT, # Cor do texto do dropdown
                                                        fill_color = ft.Colors.ON_SURFACE_VARIANT, # Cor de preenchimento do dropdown
                                                        text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'), # Estilo do texto do dropdown
                                                        on_change = lambda e: change_player_2(), # 
                                                        width = 400, # Largura do dropdown
                                                        enable_filter = True, # Permite filtrar as opções do dropdown
                                                        editable = True # Permite editar o valor do dropdown
                                                    )
                                                ]
                                            ),
                                            
                                            ft.Column(
                                                controls = [
                                                    # Texto de instrução para escolher o segundo jogador
                                                    ft.Text(
                                                        "Escolha o segundo jogador abaixo:", # Texto de instrução para escolher o segundo jogador
                                                        size = 15 # Tamanho do texto
                                                    ),
                                                    
                                                    # Dropdown para selecionar o segundo jogador
                                                    Player_2 := ft.Dropdown(
                                                        value = "Player 2", # Valor inicial do dropdown
                                                        # Opções do dropdown, começando com "Player 2"
                                                        options = [
                                                            ft.dropdown.Option("Player 2")
                                                        ] + [ft.dropdown.Option(user) for user in users["Username"].values],
                                                        
                                                        menu_height = 300, # Altura do menu do dropdown
                                                        color = ft.Colors.ON_SURFACE_VARIANT, # Cor do texto do dropdown
                                                        fill_color = ft.Colors.ON_SURFACE_VARIANT, # Cor de preenchimento do dropdown
                                                        text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'), # Estilo do texto do dropdown
                                                        on_change = lambda e: change_player_1(), # Ação a ser executada quando o valor do dropdown mudar
                                                        width = 400, # Largura do dropdown
                                                        enable_filter = True, # Permite filtrar as opções do dropdown
                                                        editable = True # Permite editar o valor do dropdown
                                                    )
                                                ]
                                            )
                                        ],

                                        alignment = ft.MainAxisAlignment.CENTER, # Alinhamento dos controles na coluna
                                        spacing = 50 # Espaçamento entre os controles na coluna
                                    )
                                ],
                                horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal da coluna
                                alignment = ft.MainAxisAlignment.CENTER, # Alinhamento vertical da coluna
                                spacing = 30 # Espaçamento entre os controles na coluna
                            ),


                            ft.Column(
                                controls = [
                                    ft.Column(
                                        controls = [
                                            # Texto de instrução para escolher os pontos necessários para vencer um set
                                            ft.Text(
                                                "Pontos por sets:", # Texto de instrução para escolher os pontos necessários para vencer um set
                                                size = 15 # Tamanho do texto
                                            ),
                                            
                                            # Dropdown para selecionar os pontos necessários para vencer um set
                                            Points_To_Win := ft.Dropdown(
                                                value = '11', # Valor inicial do dropdown
                                                # Opções do dropdown para os pontos necessários para vencer um set
                                                options = [ft.dropdown.Option(5), ft.dropdown.Option(7), ft.dropdown.Option(11), ft.dropdown.Option(21)],
                                                color = ft.Colors.ON_SURFACE_VARIANT, # Cor do texto do dropdown
                                                fill_color = ft.Colors.ON_SURFACE_VARIANT, # Cor de preenchimento do dropdown
                                                text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'), # Estilo do texto do dropdown
                                                width = 200 # Largura do dropdown
                                            )
                                        ],
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal da coluna
                                        alignment = ft.MainAxisAlignment.CENTER # Alinhamento vertical da coluna
                                    ),
                                    
                                    
                                    ft.Column(
                                        controls = [
                                            # Texto de instrução para escolher a quantidade de sets
                                            ft.Text(
                                                "Quantidade de sets:", # Texto de instrução para escolher a quantidade de sets
                                                size = 15 # Tamanho do texto
                                            ),
                                            
                                            # Dropdown para selecionar a quantidade de sets
                                            Sets := ft.Dropdown(
                                                value = '3', # Valor inicial do dropdown
                                                # Opções do dropdown para a quantidade de sets
                                                options = [ft.dropdown.Option(1), ft.dropdown.Option(3), ft.dropdown.Option(5), ft.dropdown.Option(7), ft.dropdown.Option(9)],
                                                color = ft.Colors.ON_SURFACE_VARIANT, # Cor do texto do dropdown
                                                fill_color = ft.Colors.ON_SURFACE_VARIANT, # Cor de preenchimento do dropdown
                                                text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'), # Estilo do texto do dropdown
                                                width = 200 # Largura do dropdown
                                            )
                                        ],
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal da coluna
                                        alignment = ft.MainAxisAlignment.CENTER # Alinhamento vertical da coluna
                                    )
                                ],

                                horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal da coluna
                                alignment = ft.MainAxisAlignment.CENTER # Alinhamento vertical da coluna
                            )
                        ],
                        alignment = ft.MainAxisAlignment.CENTER, # Alinhamento vertical da linha
                        spacing = 150 # Espaçamento entre os controles na linha
                    ),
                    
                    
                    # Botão flutuante para iniciar a partida
                    ft.FloatingActionButton(
                        content = ft.Text("Iniciar Partida", size = 20, color = ft.Colors.WHITE), # Conteúdo do botão flutuante
                        icon = ft.Icons.PLAY_ARROW, # Ícone do botão flutuante
                        width = 400, # Largura do botão flutuante
                        height = 50, # Altura do botão flutuante
                        bgcolor = ft.Colors.GREEN, # Cor de fundo do botão flutuante
                        on_click = lambda e: go_To_Game() # Ação do botão flutuante para iniciar a partida
                    )
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal da coluna
                alignment = ft.MainAxisAlignment.CENTER, # Alinhamento vertical da coluna
                spacing = 100 # Espaçamento entre os controles na coluna
            ),
            # height = 700,
            expand = True # Expande a tela direita para ocupar todo o espaço disponível
        )
        
        update_layout() # Atualiza o layout da página do App
    
    else:
        page.add(
            ft.Container(
                content = ft.Text(
                    "Erro ao conectar ao banco de dados! 😥", # Mensagem de erro ao conectar ao banco de dados
                    size = 30, # Tamanho do texto
                    weight = ft.FontWeight.BOLD, # Peso do texto
                ),
                alignment = ft.alignment.center, # Alinhamento do texto no centro
                expand = True # Expande o container para ocupar todo o espaço disponível
            )
        )
        page.update()


if __name__ == "__main__":
    # Inicia o App
    ft.app(target=main, name='Tênis de Mesa', use_color_emoji = True) # Inicia o App com o nome 'Tênis de Mesa' e ativa o uso de emojis coloridos