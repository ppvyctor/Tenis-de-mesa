import pandas as pd # Importa a biblioteca pandas para manipulação de dados
import flet as ft # Importa a biblioteca flet para criação do App
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
    page.window.icon = 'Icon/ping-pong.png'


    page_Home = True
    page_RankingDetalhado = False
    page_Game = False

    player_1_Code = True
    player_2_Code = True


    def change_Theme() -> None:
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        
        else:
            page.theme_mode = ft.ThemeMode.DARK
            
        page.update()


    def go_To_Home() -> None:
        nonlocal page_RankingDetalhado, page_Home, page_Game
        
        page_Game = False
        page_Home = True
        page_RankingDetalhado = False
        
        update_layout()


    def go_To_RankingDetalhado() -> None:
        nonlocal page_RankingDetalhado, page_Home, page_Game
        
        page_Game = False
        page_Home = False
        page_RankingDetalhado = True
        update_layout()


    def go_To_Game() -> None:
        nonlocal page_Game, page_Home, page_RankingDetalhado
        
        page_Game = True
        page_Home = True
        page_RankingDetalhado = False
        update_layout()


    def runSignup() -> None: 
        nonlocal page_RankingDetalhado, page_Home, page_Game
        
        page_Game = False
        page_Home = False
        page_RankingDetalhado = False
        update_layout()


    def confirme_Player_2(password: ft.TextField, alertDialog: ft.AlertDialog) -> None:
        nonlocal player_2_Code, Player_2, users

        password.error = False
        password.error_text = ""
        player_2_Code = False

        if password.value == '':
            password.error = True
            password.error_text = "Campo obrigatório"

            player_2_Code = False

        elif password.value != str(users.loc[users["Username"] == Player_2.value, "Password"].values[0]):
            password.error = True
            password.error_text = "Senha incorreta"
            Player_2.value = "Player 2"

            player_2_Code = False

        else:
            player_2_Code = True

            page.close(alertDialog)

            alertDialog = ft.AlertDialog(
                title = ft.Text("Senha Correta!"),
                content = ft.Text("Jogador 2 Já está definido!"),
                actions = [
                    ft.TextButton("Fechar", on_click=lambda e: page.close(alertDialog))
                ]
            )
            
            page.open(alertDialog)
        
        password.update()
        
        
    def confirme_Player_1(password: ft.TextField, alertDialog: ft.AlertDialog) -> None:
        nonlocal player_1_Code, Player_1, users

        password.error = False
        password.error_text = ""
        player_1_Code = False

        if password.value == '':
            password.error = True
            password.error_text = "Campo obrigatório"
            
            player_1_Code = False
        
        elif password.value != str(users.loc[users["Username"] == Player_1.value, "Password"].values[0]):
            password.error = True
            password.error_text = "Senha incorreta"
            Player_1.value = "Player 1"
            
            player_1_Code = False
        
        else:
            player_1_Code = True
            
            page.close(alertDialog)
            
            alertDialog = ft.AlertDialog(
                title = ft.Text("Senha Correta!"),
                content = ft.Text("Jogador 1 Já está definido!"),
                actions = [
                    ft.TextButton("Fechar", on_click=lambda e: page.close(alertDialog))
                ]
            )
            
            page.open(alertDialog)
        
        password.update()
    
    
    def change_player_1() -> None:
        nonlocal Player_1, Player_2, users, player_2_Code
        
        
        player_2_Code = False
        
        if Player_2.value != "Player 2":
            alertDialog = ft.AlertDialog(
                title = ft.Text("Digite a senha da conta!"),
                content = ft.Text("Digite a senha cadastrada ao criar sua conta no aplicativo. Caso tenha esquecido, entre em contato com o responsável pelo APP."),
                actions = [
                    password := ft.TextField(
                        label = "Confirme sua senha: ",
                        hint_text = "Digite sua senha",
                        max_length = 100,
                        prefix_icon = ft.Icons.LOCK,
                        keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD,
                        color = ft.Colors.ON_SURFACE_VARIANT,
                        password = True,
                        can_reveal_password = True,
                        width = 400,
                        border = ft.InputBorder.UNDERLINE,
                        input_filter = ft.InputFilter(
                            regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$',
                            allow = False
                        ),
                        on_submit = lambda e: confirme_Player_2(password, alertDialog)
                    ),
                    
                    ft.FloatingActionButton(
                        content = ft.Text("Confirmar Senha", color = ft.Colors.WHITE, weight = 'bold', size = 20),
                        bgcolor = ft.Colors.BLUE,
                        width = 240,
                        height = 40,
                        on_click = lambda e: confirme_Player_2(password, alertDialog)
                    )
                ],
                actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            )
            
            page.open(alertDialog)
        
        else:
            player_2_Code = True
        
            
        Player_1.options = [ft.dropdown.Option("Player 1")] + [ft.dropdown.Option(user) for user in users["Username"] if Player_2.value != user]
        page.update()
        
    
    def change_player_2() -> None:
        nonlocal Player_1, player_1_Code, Player_2, users
        
        
        player_1_Code = False
        
        if Player_1.value != "Player 1":
            alertDialog = ft.AlertDialog(
                title = ft.Text("Digite a senha da conta!"),
                content = ft.Text("Digite a senha cadastrada ao criar sua conta no aplicativo. Caso tenha esquecido, entre em contato com o responsável pelo APP."),
                actions = [
                    password := ft.TextField(
                        label = "Confirme sua senha: ",
                        hint_text = "Digite sua senha",
                        max_length = 100,
                        prefix_icon = ft.Icons.LOCK,
                        keyboard_type = ft.KeyboardType.VISIBLE_PASSWORD,
                        color = ft.Colors.ON_SURFACE_VARIANT,
                        password = True,
                        can_reveal_password = True,
                        width = 400,
                        border = ft.InputBorder.UNDERLINE,
                        input_filter = ft.InputFilter(
                            regex_string = r'^[a-zA-Z0-9_@$!%*?&#]*$',
                            allow = False
                        ),
                        on_submit = lambda e: confirme_Player_1(password, alertDialog)
                    ),

                    ft.FloatingActionButton(
                        content = ft.Text("Confirmar Senha", color = ft.Colors.WHITE, weight = 'bold', size = 20),
                        bgcolor = ft.Colors.BLUE,
                        width = 240,
                        height = 40,
                        on_click = lambda e: confirme_Player_1(password, alertDialog)
                    )
                ],
                actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            )
            page.open(alertDialog)
            
        else:
            player_1_Code = True
        
        
        Player_2.options = [ft.dropdown.Option("Player 2")] + [ft.dropdown.Option(user) for user in users["Username"] if Player_1.value != user]
        page.update()
    
    
    def update_layout() -> None:
        nonlocal users, Player_1, Player_2, page_Game
        
        page.clean()
        
        if page_Home:
            
            if page_Game:
                if not player_1_Code and not player_2_Code:
                    
                    alert = ft.AlertDialog(
                        title = ft.Text("Jogadores não definidos!"),
                        content = ft.Text(f"Ambos jogadores devem ser definidos para continuar!"),
                        actions = [
                            ft.TextButton("Fechar", on_click=lambda e: page.close(alert))
                        ]
                    )
                    page_Game = False
                    page.add(ft.Row(controls = [left_screen, right_screen], expand = True))
                    
                    page.open(alert)
                    
                elif not player_1_Code:
                    
                    alert = ft.AlertDialog(
                        title = ft.Text("Jogador não definido!"),
                        content = ft.Text(f"Jogador 1 precisa ser definido para continuar!"),
                        actions = [
                            ft.TextButton("Fechar", on_click=lambda e: page.close(alert))
                        ]
                    )
                    page_Game = False
                    page.add(ft.Row(controls = [left_screen, right_screen], expand = True))
                    
                    page.open(alert)
                
                elif not player_2_Code:
                    
                    alert = ft.AlertDialog(
                        title = ft.Text("Jogador não definido!"),
                        content = ft.Text(f"Jogador 2 precisa ser definido para continuar!"),
                        actions = [
                            ft.TextButton("Fechar", on_click=lambda e: page.close(alert))
                        ]
                    )
                    page_Game = False
                    page.add(ft.Row(controls = [left_screen, right_screen], expand = True))
                    
                    page.open(alert)
                    
                
                else:
                    page.add(
                        ft.Row(
                            controls = [
                                left_screen,
                                
                                
                                ft.Column(
                                    controls = [
                                        ft.Row(
                                            controls = [
                                                ft.IconButton(
                                                    icon = ft.Icons.CLOSE,
                                                    tooltip = 'Encerrar partida',
                                                    icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                                    icon_size = 60,
                                                    on_click = lambda e: go_To_Home()
                                                ),
                                                
                                                
                                                ft.IconButton(
                                                    icon = ft.Icons.REFRESH,
                                                    tooltip = 'Reiniciar partida',
                                                    icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                                    icon_size = 60,
                                                    alignment = ft.alignment.center_right,
                                                    on_click = lambda e: go_To_Game()
                                                ),
                                            ],
                                            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                                        ),
                                        
                                        game(page, Player_1.value, Player_2.value, Points_To_Win.value, Sets.value)
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                                    expand = True
                                )
                            ],
                            expand = True
                        )
                    )
            
            else:
                page.add(ft.Row(controls = [left_screen, right_screen], expand = True))
                
                
                if not os.path.exists("Users"): os.makedirs("Users")
                
                try:
                    users = pd.read_excel("Users/users.xlsx").sort_values('Username', ascending = True).reset_index(drop = True)
                except:
                    users = pd.DataFrame(columns=["Username", 'Password', 'Wins', 'Defeats', 'Scores'])
                    users.to_excel("Users/users.xlsx", index = False)
                
                users = users.sort_values('Username', ascending = True, key = lambda user: user.str.lower()).reset_index(drop = True)
                
                Player_1.options = [ft.dropdown.Option("Player 1")] + [ft.dropdown.Option(user) for user in users["Username"].values if Player_2.value != user]
                Player_2.options = [ft.dropdown.Option("Player 2")] + [ft.dropdown.Option(user) for user in users["Username"].values if Player_1.value != user]
        
        
        elif page_RankingDetalhado:
            page.add(ft.Row(controls = [left_screen, RankingDetalhado(page)], expand = True))
        
            
        else:
            page.add(ft.Row(controls = [left_screen, Signup(page)], expand = True))
        
        
        page.update()
    
    # Conteúdo a esquerda do App
    left_screen = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Column(
                        controls = [
                            ft.IconButton(
                                icon = ft.Icons.MENU,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 45,
                                height = 50,
                                alignment = ft.alignment.center
                            ),
                            
                            ft.IconButton(
                                tooltip = "Página Inicial",
                                icon = ft.Icons.SPORTS_ESPORTS,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 35,
                                height = 50,
                                alignment = ft.alignment.center,
                                on_click = lambda e: go_To_Home()
                            ),
                            
                            ft.IconButton(
                                tooltip = "Cadastrar",
                                icon = ft.Icons.PERSON_ADD,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 35,
                                height = 50,
                                alignment = ft.alignment.center,
                                on_click = lambda e: runSignup()
                            ),
                            
                            ft.IconButton(
                                tooltip = "Remover Jogador",
                                icon = ft.Icons.PERSON_REMOVE,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 35,
                                height = 50,
                                alignment = ft.alignment.center
                                #on_click = lambda e: runSignup()
                            ),
                            
                            ft.IconButton(
                                tooltip = "Ranking Completo dos Jogadores",
                                icon = ft.Icons.EMOJI_EVENTS,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 35,
                                on_click = lambda e: go_To_RankingDetalhado(),
                                height = 50,
                                alignment = ft.alignment.center
                            )
                        ]
                    ),
                    
                    ft.Column(
                        controls = [
                            ft.IconButton(
                                tooltip = "Mudar tema",
                                icon = ft.Icons.BRIGHTNESS_6,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 25,
                                on_click = lambda e: change_Theme(),
                                height = 50,
                                alignment = ft.alignment.center
                            ),
                            
                            ft.IconButton(
                                tooltip = "Sair",
                                icon = ft.Icons.EXIT_TO_APP,
                                icon_color = ft.Colors.ON_SURFACE_VARIANT,
                                icon_size = 25,
                                on_click = lambda e: page.window.close(),
                                height = 50,
                                alignment = ft.alignment.center
                            )
                        ]
                    )
                ],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            width = 50
        )
    
    if not os.path.exists("Users"): os.makedirs("Users")
    
    try:
        users = pd.read_excel("Users/users.xlsx")
    except:
        users = pd.DataFrame(columns=["Username", "Password", "Wins", "Defeats", "Scores"])
        users.to_excel("Users/users.xlsx", index = False)
    
    users = users.sort_values('Username', ascending = True, key = lambda user: user.str.lower()).reset_index(drop = True)
    
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
                                                    "Escolha o primeiro jogador abaixo:",
                                                    size = 15
                                                ),
                                                
                                                Player_1 := ft.Dropdown(
                                                    value = "Player 1",
                                                    options = [
                                                        ft.dropdown.Option("Player 1")
                                                    ] + [ft.dropdown.Option(user) for user in users["Username"].values],
                                                    menu_height = 300,
                                                    color = ft.Colors.ON_SURFACE_VARIANT,
                                                    fill_color = ft.Colors.ON_SURFACE_VARIANT,
                                                    text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'),
                                                    on_change = lambda e: change_player_2(),
                                                    width = 400,
                                                    enable_filter = True,
                                                    editable = True
                                                )
                                            ]
                                        ),
                                        
                                        ft.Column(
                                            controls = [
                                                ft.Text(
                                                    "Escolha o segundo jogador abaixo:",
                                                    size = 15
                                                ),
                                                
                                                Player_2 := ft.Dropdown(
                                                    value = "Player 2",
                                                    options = [
                                                        ft.dropdown.Option("Player 2")
                                                    ] + [ft.dropdown.Option(user) for user in users["Username"].values],
                                                    
                                                    menu_height = 300,
                                                    color = ft.Colors.ON_SURFACE_VARIANT,
                                                    fill_color = ft.Colors.ON_SURFACE_VARIANT,
                                                    text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'),
                                                    on_change = lambda e: change_player_1(),
                                                    width = 400,
                                                    enable_filter = True,
                                                    editable = True
                                                )
                                            ]
                                        )
                                    ],

                                    alignment = ft.MainAxisAlignment.CENTER,
                                    spacing = 50
                                )
                            ],
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            alignment = ft.MainAxisAlignment.CENTER,
                            spacing = 30
                        ),


                        ft.Column(
                            controls = [
                                ft.Column(
                                    controls = [
                                        ft.Text(
                                            "Pontos por sets:",
                                            size = 15
                                        ),
                                        
                                        Points_To_Win := ft.Dropdown(
                                            value = '11',
                                            options = [ft.dropdown.Option(5), ft.dropdown.Option(7), ft.dropdown.Option(11), ft.dropdown.Option(21)],
                                            color = ft.Colors.ON_SURFACE_VARIANT,
                                            fill_color = ft.Colors.ON_SURFACE_VARIANT,
                                            text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'),
                                            width = 200
                                        )
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    alignment = ft.MainAxisAlignment.CENTER
                                ),
                                
                                
                                ft.Column(
                                    controls = [
                                        ft.Text(
                                            "Quantidade de sets:",
                                            size = 15
                                        ),
                                        
                                        Sets := ft.Dropdown(
                                            value = '1',
                                            options = [ft.dropdown.Option(1), ft.dropdown.Option(3), ft.dropdown.Option(5), ft.dropdown.Option(7), ft.dropdown.Option(9)],
                                            color = ft.Colors.ON_SURFACE_VARIANT,
                                            fill_color = ft.Colors.ON_SURFACE_VARIANT,
                                            text_style = ft.TextStyle(color = ft.Colors.BLACK, size = 17, weight = 'bold'),
                                            width = 200
                                        )
                                    ],
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                    alignment = ft.MainAxisAlignment.CENTER
                                )
                            ],
                            
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                            alignment = ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 150
                ),
                
                
                ft.FloatingActionButton(
                    content = ft.Text("Iniciar Partida", size = 20, color = ft.Colors.WHITE),
                    icon = ft.Icons.PLAY_ARROW,
                    width = 400,
                    height = 50,
                    bgcolor = ft.Colors.GREEN,
                    on_click = lambda e: go_To_Game()
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,
            spacing = 100
        ),
        # height = 700,
        expand = True
    )
    
    update_layout()
    


if __name__ == "__main__":
    # Inicia o App
    ft.app(target=main, name='Tênis de Mesa', use_color_emoji = True)