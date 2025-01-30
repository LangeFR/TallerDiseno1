# tallerdiseno1/views/inscripcion_view.py

import flet as ft

def create_inscripcion_view(inscribir_persona, validar_identificacion, validar_email, validar_apellidos):
    """
    Crea y retorna la vista de inscripción de miembros.
    
    Parámetros:
        inscribir_persona (function): Función callback para manejar la inscripción.
        validar_identificacion (function): Función para validar la identificación.
        validar_email (function): Función para validar el correo electrónico.
        validar_apellidos (function): Función para validar los apellidos.
    
    Retorna:
        ft.Column: La vista de inscripción como un objeto Column de Flet.
    """
    
    nombre_field = ft.TextField(
        label="Nombre", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True
    )
    
    apellidos_field = ft.TextField(
        label="Apellidos", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_apellidos
    )
    
    edad_field = ft.TextField(
        label="Edad", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_identificacion,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    id_field = ft.TextField(
        label="Número de identificación", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_identificacion,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    correo_field = ft.TextField(
        label="Correo", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_email
    )
    
    telefono_field = ft.TextField(
        label="Teléfono", 
        width=400, 
        border_color=ft.colors.OUTLINE, 
        expand=True, 
        on_change=validar_identificacion,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    inscribir_button = ft.ElevatedButton(
        "Inscribir",
        on_click=inscribir_persona,
        icon=ft.icons.PERSON_ADD,
        bgcolor=ft.colors.PRIMARY,
        color=ft.colors.WHITE,
    )
    
    inscripcion_view = ft.Column(
        [
            ft.Text("Inscripción de Miembros", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            nombre_field,
            apellidos_field,  # Añadido 'apellidos_field'
            edad_field,
            id_field,
            correo_field,
            telefono_field,
            inscribir_button,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )
    
    return inscripcion_view, nombre_field, apellidos_field, edad_field, id_field, correo_field, telefono_field
