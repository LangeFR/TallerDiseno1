import flet as ft

def create_entrenamientos_view(controller):
    """
    Crea y retorna la vista de gestión de entrenamientos, incluyendo los componentes internos.
    
    Parámetros:
        controller (ClubController): Controlador que maneja la lógica de negocio.
    
    Retorna:
        tuple: Contiene la vista de entrenamientos y los componentes necesarios como objetos de Flet.
    """
    # Crear dropdown para seleccionar usuarios
    dropdown_usuarios = ft.Dropdown(
        label="Seleccione un Usuario",
        options=[ft.dropdown.Option(user.nombre) for user in controller.usuarios]
    )
    
    # Crear dropdown para seleccionar entrenamientos
    entrenamientos = controller.cargar_entrenamientos()
    dropdown_entrenamientos = ft.Dropdown(
        label="Seleccione un entrenamiento",
        options=[ft.dropdown.Option(ent.fecha) for ent in entrenamientos]
    )
    
    # Crear botón para inscribir a entrenamiento
    def inscribir_a_entrenamiento(e):
        print("Inscripción a entrenamiento iniciada")
    
    # Lista para mostrar entrenamientos disponibles
    entrenamientos_list = ft.Column(
        [ft.Text(ent.fecha) for ent in entrenamientos]
    )
    
    inscribir_entrenamiento_button = ft.ElevatedButton(
        "Inscribir en Entrenamiento",
        icon=ft.icons.CHECK,
        on_click=inscribir_a_entrenamiento
    )
    
    # Vista para asistencias registradas
    asistencias_list = ft.Column([])
    
    asistencias_view = ft.Container(
        ft.Column(
            [
                ft.Text("Asistencias Registradas", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                asistencias_list,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        expand=True,
        padding=20,
    )
    
    # Vista principal de entrenamientos
    entrenamientos_view = ft.Row(
        [
            ft.Container(
                content=ft.Column(
                    [
                        dropdown_usuarios,
                        dropdown_entrenamientos,
                        inscribir_entrenamiento_button,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=300,
                padding=20,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=10,
            ),
            ft.VerticalDivider(width=1),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Entrenamientos Disponibles", size=24, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10, thickness=2),
                        entrenamientos_list,
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.START,
                ),
                expand=True,
                padding=20,
            ),
            ft.VerticalDivider(width=1),
            asistencias_view,
        ],
        expand=True,
    )
    
    return entrenamientos_view, entrenamientos_list, dropdown_entrenamientos
