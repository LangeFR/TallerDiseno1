import flet as ft

def main(page: ft.Page):
    # Paleta de colores extraída de Coolors
    COLOR_DARK_PURPLE = "#89023e"   # Para elementos destacados y el botón de admin
    COLOR_MUTED_PINK = "#cc7178"    # Para el botón de entrenador
    COLOR_LIGHT_PINK = "#ffd9da"    # Para el fondo de la página
    COLOR_PALE_PINK = "#f3e1dd"     # Para el fondo del contenedor principal
    COLOR_SOFT_GREEN = "#9FAE92"    # Verde para el botón de usuario, tono más oscuro

    # Configuración de la página
    page.title = "Inicio de Sesión - Roles"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = COLOR_LIGHT_PINK

    # Variables de estado
    view_mode = "login"  # "login" o "register"
    selected_role = ""

    # AnimatedSwitcher para el formulario de login (parte de la vista login)
    login_form_switcher = ft.AnimatedSwitcher(
        duration=300,
        transition=ft.AnimatedSwitcherTransition.FADE,
        content=ft.Container(key="empty")
    )

    # Función que genera el formulario de login (con el rol actualizado)
    def get_login_form():
        return ft.Container(
            key="login_form",
            content=ft.Column(
                controls=[
                    ft.Text(
                        value=f"Iniciar sesión como: {selected_role.upper()}",
                        size=18,
                        weight=ft.FontWeight.W_600,
                        color=COLOR_DARK_PURPLE
                    ),
                    ft.TextField(label="Usuario", width=300),
                    ft.TextField(label="Contraseña", password=True, width=300),
                    ft.ElevatedButton(
                        text="Ingresar",
                        width=300,
                        bgcolor=COLOR_DARK_PURPLE,
                        color="white"
                    )
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(10)
        )

    # Función que se invoca al seleccionar un rol en la vista login
    def on_role_click(e, role):
        nonlocal selected_role
        selected_role = role
        login_form_switcher.content = get_login_form()
        page.update()

    # Función auxiliar para crear botones con icono y texto dispuestos verticalmente
    def vertical_button(icon, label, role, bgcolor):
        return ft.ElevatedButton(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=40, color="white"),
                    ft.Text(label, size=14, color="white")
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            on_click=lambda e: on_role_click(e, role),
            bgcolor=bgcolor,
            width=150
        )

    # Fila de botones para seleccionar rol (vista de Login)
    roles_row = ft.Row(
        controls=[
            vertical_button(ft.Icons.ADMIN_PANEL_SETTINGS, "ADMINISTRADOR", "admin", COLOR_DARK_PURPLE),
            vertical_button(ft.Icons.SPORTS_TENNIS, "ENTRENADOR", "coach", COLOR_MUTED_PINK),
            vertical_button(ft.Icons.PERSON, "USUARIO", "user", COLOR_SOFT_GREEN)
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Vista de Login: formulario (si se selecciona rol), botones y enlace para registrarse
    def get_login_view():
        return ft.Column(
            controls=[
                login_form_switcher,
                ft.Divider(height=20, color=COLOR_DARK_PURPLE),
                roles_row,
                ft.TextButton(
                    "¿No te has registrado? ¡Crea tu cuenta!",
                    on_click=lambda e: switch_to_register()
                )
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

    # Vista de Registro: formulario de registro con campos y enlace para volver al login
    def get_register_view():
        return ft.Column(
            controls=[
                ft.Text("Registro", size=20, weight=ft.FontWeight.W_600, color=COLOR_DARK_PURPLE),
                ft.TextField(label="Nombre completo", width=300),
                ft.TextField(label="Correo electrónico", width=300),
                ft.TextField(label="Teléfono", width=300),
                ft.TextField(label="Contraseña", password=True, width=300),
                ft.TextField(label="Verificar contraseña", password=True, width=300),
                ft.Dropdown(
                    label="Selecciona tu rol",
                    width=300,
                    options=[
                        ft.dropdown.Option("admin", "Administrador"),
                        ft.dropdown.Option("coach", "Entrenador"),
                        ft.dropdown.Option("user", "Usuario")
                    ]
                ),
                ft.ElevatedButton(
                    text="Registrarse",
                    width=300,
                    bgcolor=COLOR_DARK_PURPLE,
                    color="white"
                ),
                ft.TextButton(
                    "¿Ya tienes cuenta? Inicia sesión",
                    on_click=lambda e: switch_to_login()
                )
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            key="register_view"
        )

    # Funciones para cambiar la vista
    def switch_to_register():
        nonlocal view_mode
        view_mode = "register"
        update_main_switcher()

    def switch_to_login():
        nonlocal view_mode
        view_mode = "login"
        # Reiniciamos el login_form_switcher (vuelve a estar vacío)
        login_form_switcher.content = ft.Container(key="empty")
        update_main_switcher()

    # Actualiza el contenido del main_switcher según la vista actual
    def update_main_switcher():
        if view_mode == "login":
            main_switcher.content = get_login_view()
        else:
            main_switcher.content = get_register_view()
        page.update()

    # AnimatedSwitcher principal para alternar entre las vistas de login y registro
    main_switcher = ft.AnimatedSwitcher(
        duration=300,
        transition=ft.AnimatedSwitcherTransition.FADE,
        content=get_login_view()
    )

    # Contenedor "card" estilizado que envuelve la vista principal con width ajustado a 600
    container = ft.Container(
        content=main_switcher,
        width=600,
        padding=20,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),
        bgcolor=COLOR_PALE_PINK,
        border=ft.border.all(2, COLOR_DARK_PURPLE),
        shadow=ft.BoxShadow(
            color=COLOR_DARK_PURPLE,
            blur_radius=10,
            spread_radius=1,
            offset=ft.Offset(2, 2)
        )
    )

    page.add(container)

if __name__ == "__main__":
    ft.app(target=main)
