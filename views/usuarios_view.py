# tallerdiseno1/views/usuarios_view.py

import flet as ft

def create_usuarios_view(mostrar_usuarios_view):
    """
    Crea y retorna la vista de gestión de usuarios.
    
    Parámetros:
        mostrar_usuarios_view (function): Función para mostrar usuarios filtrados.
    
    Retorna:
        ft.Column: La vista de usuarios como un objeto Column de Flet.
    """
    
    matriculados_button = ft.ElevatedButton(
        "Mostrar Matriculados", 
        on_click=lambda e: mostrar_usuarios_view("matriculado")
    )
    
    inscritos_button = ft.ElevatedButton(
        "Mostrar Inscritos", 
        on_click=lambda e: mostrar_usuarios_view("inscrito")
    )
    
    Usuarios_view = ft.Column(
        [
            ft.Text("Usuarios", size=20, weight=ft.FontWeight.BOLD),
            matriculados_button,
            inscritos_button
        ],
        spacing=10
    )
    
    return Usuarios_view
