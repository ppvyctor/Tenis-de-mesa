import flet as ft
import pandas as pd

def game(
    page: ft.Page,
    Player_1: str,
    Player_2: str,
    Points_To_Win: str,
    Sets: str
):
    Container_Game = ft.Ref[ft.Container]()
    Draw = False
    
    
    
    def sum_Point_Player1():
        nonlocal Draw
        
        point_Player1.value = str(int(point_Player1.value) + 1)
        
        if point_Player1.value == str(int(Points_To_Win) - 1) and point_Player2.value == str(int(Points_To_Win) - 1): 
            Draw = True
        
        update_layout()
        
    
    def sum_Point_Player2():
        nonlocal Draw
        
        point_Player2.value = str(int(point_Player2.value) + 1)
        
        if point_Player1.value == str(int(Points_To_Win) - 1) and point_Player2.value == str(int(Points_To_Win) - 1): 
            Draw = True
        
        update_layout()


    def update_layout():
        nonlocal Container_Game, Draw
        
        if Draw:
            if int(point_Player1.value) - int(point_Player2.value) == 2:
                set_Player1.value = str(int(set_Player1.value) + 1)
                Draw = False
                point_Player1.value = '0'
                point_Player2.value = '0'
            
            elif int(point_Player2.value) - int(point_Player1.value) == 2:
                set_Player2.value = str(int(set_Player2.value) + 1)
                Draw = False
                point_Player1.value = '0'
                point_Player2.value = '0'
                
        else:      
            if point_Player1.value == Points_To_Win:
                set_Player1.value = str(int(set_Player1.value) + 1)
                point_Player1.value = '0'
                point_Player2.value = '0'
            
            elif point_Player2.value == Points_To_Win:
                set_Player2.value = str(int(set_Player2.value) + 1)
                point_Player1.value = '0'
                point_Player2.value = '0'
        
        
        if set_Player1.value == Sets:
            Container_Game.current.content = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text(
                            "PARABÉNS " + Player_1 + ', VOCÊ GANHOU! 🎉🎉',
                            size = 40,
                            weight = 'bold',
                            color = ft.Colors.ON_SURFACE_VARIANT
                        )
                    ],
                    
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                expand = True
            )
            
            
            if Player_1 != 'Player 1':
                try:
                    users = pd.read_excel(r'Users/users.xlsx')
                    
                except:
                    try:
                        users = pd.read_excel(r'Users\\users.xlsx')
                        
                    except:
                        try:
                            users = pd.DataFrame(columns=['Username', 'Email', 'Password', 'Wins', 'Defeats', 'Scores'])
                            users.to_excel(r'Users/users.xlsx', index=False)
                        except:
                            users = pd.DataFrame(columns=['Username', 'Email', 'Password', 'Wins', 'Defeats', 'Scores'])
                            users.to_excel(r'Users\\users.xlsx', index=False)
                
                
                users.loc[users['Username'] == Player_1, 'Wins'] += 1
                users.loc[users['Username'] == Player_1, 'Scores'] += 3
                
                if Player_2 != 'Player 2': users.loc[users['Username'] == Player_2, 'Defeats'] += 1
                
                try:
                    users.to_excel(r'Users/users.xlsx', index=False)
                    
                except:
                    users.to_excel(r'Users\\users.xlsx', index=False) 
                
            
            
        
        elif set_Player2.value == Sets:
            Container_Game.current.content = ft.Container(
                content = ft.Column(
                    controls = [
                        ft.Text(
                            "PARABÉNS " + Player_2 + ', VOCÊ GANHOU! 🎉🎉',
                            size = 40,
                            weight = 'bold',
                            color = ft.Colors.ON_SURFACE_VARIANT
                        )
                    ],
                    
                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                    alignment = ft.MainAxisAlignment.CENTER
                ),
                expand = True
            )
            
            
            if Player_2 != 'Player 2':
                try:
                    users = pd.read_excel(r'Users/users.xlsx')
                    
                except:
                    try:
                        users = pd.read_excel(r'Users\\users.xlsx')
                        
                    except:
                        try:
                            users = pd.DataFrame(columns=['Username', 'Email', 'Password', 'Wins', 'Defeats', 'Scores'])
                            users.to_excel(r'Users/users.xlsx', index=False)
                        except:
                            users = pd.DataFrame(columns=['Username', 'Email', 'Password', 'Wins', 'Defeats', 'Scores'])
                            users.to_excel(r'Users\\users.xlsx', index=False)
                
                
                users.loc[users['Username'] == Player_2, 'Wins'] += 1
                users.loc[users['Username'] == Player_2, 'Scores'] += 3
                
                if Player_1 != 'Player 1': users.loc[users['Username'] == Player_1, 'Defeats'] += 1
                
                try:
                    users.to_excel(r'Users/users.xlsx', index=False)
                    
                except:
                    users.to_excel(r'Users\\users.xlsx', index=False)
                    
                
                
            
        page.update()
            
    
    
    Container_Game.current = ft.Container(
        content = ft.Column(
            controls = [
                ft.Row(
                    controls = [
                        ft.Row(
                            controls = [
                                point_Player1 := ft.Text(
                                    "0",
                                    size = 200,
                                    weight = 'bold'
                                ),
                                
                                
                                set_Player1 := ft.Text(
                                    "0",
                                    size = 50
                                )
                            ],
                            spacing = 80,
                            alignment = ft.MainAxisAlignment.CENTER
                        ),
                        
                        ft.Text(
                            "VS",
                            size = 30,
                            weight = "bold"
                        ),
                        
                        ft.Row(
                            controls = [
                                set_Player2 := ft.Text(
                                    "0",
                                    size = 50
                                ),
                                
                                point_Player2 := ft.Text(
                                    "0",
                                    size = 200,
                                    weight = 'bold'
                                )
                            ],
                            spacing = 80,
                            alignment = ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                    spacing = 100
                ),
                
                
                ft.Row(
                    controls = [
                        ft.FloatingActionButton(
                            content = ft.Text(Player_1, color = ft.Colors.WHITE, size = 30),
                            tooltip = 'Somar 1 ponto para ' + Player_1,
                            bgcolor = ft.Colors.GREEN,
                            height = 100,
                            expand = True,
                            on_click = lambda e: sum_Point_Player1()
                        ),
                        
                        ft.Text(
                            '           ',
                            size = 50,
                            weight = "bold"
                        ),
                        
                        ft.FloatingActionButton(
                            content = ft.Text(Player_2, color = ft.Colors.WHITE, size = 30),
                            tooltip = 'Somar 1 ponto para ' + Player_2,
                            bgcolor = ft.Colors.GREEN,
                            height = 100,
                            expand = True,
                            on_click = lambda e: sum_Point_Player2()
                        )
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment = ft.MainAxisAlignment.CENTER,
            expand = True
        ),
        expand = True
    )
    
    update_layout()
    
    
    return Container_Game.current