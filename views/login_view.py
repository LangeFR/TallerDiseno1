import flet as ft
from modelos.usuario import Usuario
from controllers import auth_controller

def main(page: ft.Page):
    # Paleta de colores extraída de Coolors
    COLOR_DARK_PURPLE = "#89023e"   # Elementos destacados y botón de admin
    COLOR_MUTED_PINK = "#cc7178"    # Botón de entrenador
    COLOR_LIGHT_PINK = "#ffd9da"    # Fondo de la página
    COLOR_PALE_PINK = "#f3e1dd"     # Fondo del contenedor principal
    COLOR_SOFT_GREEN = "#9FAE92"    # Botón de usuario, tono más oscuro

    page.title = "Inicio de Sesión - Roles"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = COLOR_LIGHT_PINK

    view_mode = "login"  # Puede ser "login" o "register"
    selected_role = ""

    # AnimatedSwitcher para el formulario de login (se muestra cuando se selecciona un rol)
    login_form_switcher = ft.AnimatedSwitcher(
        duration=300,
        transition=ft.AnimatedSwitcherTransition.FADE,
        content=ft.Container(key="empty")
    )

    # AnimatedSwitcher para el logo (visible solo en la vista de login)
    logo_switcher = ft.AnimatedSwitcher(
        duration=300,
        transition=ft.AnimatedSwitcherTransition.FADE,
        content=ft.Image(src="views/SpinTrackerLogo.jpeg", width=200, margin=ft.margin.only(top=20))
    )

    # Función que genera el formulario de login (usa el rol seleccionado)
    def get_login_form():
        # Campos para correo y contraseña (en este ejemplo se usa el correo como identificador)
        correo_field = ft.TextField(label="Correo", width=300, key="correo_field")
        password_field = ft.TextField(label="Contraseña", password=True, width=300, key="password_field")
        login_button = ft.ElevatedButton(
            text="Ingresar",
            width=300,
            bgcolor=COLOR_DARK_PURPLE,
            color="white",
            on_click=lambda e: on_login(correo_field.value, password_field.value)
        )
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
                    correo_field,
                    password_field,
                    login_button
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.all(10)
        )

    # Función que se invoca al hacer login
    def on_login(correo, contrasena):
        usuario_valido = auth_controller.validar_login(correo, contrasena)
        if usuario_valido is None:
            page.snack_bar = ft.SnackBar(content=ft.Text("Credenciales incorrectas"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Login exitoso"))
            page.snack_bar.open = True
            page.update()
            # Aquí se puede invocar la interfaz administrativa, por ejemplo:
            print("Usuario autenticado:", usuario_valido)
            # O bien, cambiar el contenido de la página para cargar la vista de 'tenis.py'

    # Función que se invoca al seleccionar un rol en la vista de login
    def on_role_click(e, role):
        nonlocal selected_role
        selected_role = role
        login_form_switcher.content = get_login_form()
        page.update()

    # Función auxiliar para crear botones con icono y texto en disposición vertical
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

    # Fila de botones para seleccionar el rol (vista de Login)
    roles_row = ft.Row(
        controls=[
            vertical_button(ft.Icons.ADMIN_PANEL_SETTINGS, "ADMINISTRADOR", "admin", COLOR_DARK_PURPLE),
            vertical_button(ft.Icons.SPORTS_TENNIS, "ENTRENADOR", "coach", COLOR_MUTED_PINK),
            vertical_button(ft.Icons.PERSON, "USUARIO", "user", COLOR_SOFT_GREEN)
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Vista de Login: incluye formulario, botones de rol y enlace para registrarse
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

    # Vista de Registro: formulario de registro y enlace para volver al login
    def get_register_view():
        nombre_field = ft.TextField(label="Nombre completo", width=300, key="nombre_field")
        correo_field = ft.TextField(label="Correo electrónico", width=300, key="correo_field")
        telefono_field = ft.TextField(label="Teléfono", width=300, key="telefono_field")
        contrasena_field = ft.TextField(label="Contraseña", password=True, width=300, key="contrasena_field")
        verificar_field = ft.TextField(label="Verificar contraseña", password=True, width=300, key="verificar_field")
        rol_dropdown = ft.Dropdown(
            label="Selecciona tu rol",
            width=300,
            key="rol_dropdown",
            options=[
                ft.dropdown.Option("admin", "Administrador"),
                ft.dropdown.Option("coach", "Entrenador"),
                ft.dropdown.Option("user", "Usuario")
            ]
        )
        register_button = ft.ElevatedButton(
            text="Registrarse",
            width=300,
            bgcolor=COLOR_DARK_PURPLE,
            color="white",
            on_click=lambda e: on_register(
                nombre_field.value,
                correo_field.value,
                telefono_field.value,
                contrasena_field.value,
                verificar_field.value,
                rol_dropdown.value
            )
        )
        return ft.Column(
            controls=[
                ft.Text("Registro de Usuario", size=20, weight=ft.FontWeight.W_600, color=COLOR_DARK_PURPLE),
                nombre_field,
                correo_field,
                telefono_field,
                contrasena_field,
                verificar_field,
                rol_dropdown,
                register_button,
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

    # Función para procesar el registro
    def on_register(nombre, correo, telefono, contrasena, verificar, rol):
        if contrasena != verificar:
            page.snack_bar = ft.SnackBar(content=ft.Text("Las contraseñas no coinciden"))
            page.snack_bar.open = True
            page.update()
            return
        nuevo_usuario = Usuario(
            id=Usuario.nuevo_id(),
            nombre=nombre,
            apellidos="",
            edad=0,
            num_identificacion="",
            correo=correo,
            telefono=telefono,
            estado="inscrito",
            rol=rol,
            contrasena=contrasena
        )
        success = auth_controller.registrar_usuario(nuevo_usuario)
        if not success:
            page.snack_bar = ft.SnackBar(content=ft.Text("Ya existe un usuario con ese correo"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Registro exitoso! Inicia sesión"))
            page.snack_bar.open = True
            page.update()
            switch_to_login()

    # Funciones para cambiar de vista
    def switch_to_register():
        nonlocal view_mode
        view_mode = "register"
        update_main_switcher()

    def switch_to_login():
        nonlocal view_mode
        view_mode = "login"
        login_form_switcher.content = ft.Container(key="empty")
        update_main_switcher()

    def update_main_switcher():
        if view_mode == "login":
            main_switcher.content = get_login_view()
            logo_switcher.content = ft.Image(src="views/SpinTrackerLogo.jpeg", width=200, margin=ft.margin.only(top=20))
        else:
            main_switcher.content = get_register_view()
            logo_switcher.content = ft.Container(key="empty")
        page.update()

    # AnimatedSwitcher principal para alternar entre las vistas de login y registro
    main_switcher = ft.AnimatedSwitcher(
        duration=300,
        transition=ft.AnimatedSwitcherTransition.FADE,
        content=get_login_view()
    )

    # Contenedor "card" que agrupa el logo (mediante logo_switcher) y la vista principal, con width ajustado a 600
    container = ft.Container(
        content=ft.Column(
            controls=[
                logo_switcher,
                main_switcher
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
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
