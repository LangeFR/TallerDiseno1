import flet as ft

def main(page: ft.Page):
    # Paleta de colores extraída de Coolors
    COLOR_DARK_PURPLE = "#89023e"   # Para elementos destacados y el botón de admin
    COLOR_MUTED_PINK = "#cc7178"    # Para el botón de entrenador
    COLOR_LIGHT_PINK = "#ffd9da"    # Para el fondo de la página
    COLOR_PALE_PINK = "#f3e1dd"     # Para el fondo del contenedor principal
    COLOR_SOFT_GREEN = "#9fad92"    # Para el botón de usuario

    # Configuración de la página
    page.title = "Inicio de Sesión - Roles"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = COLOR_LIGHT_PINK

    # Variable de estado para el rol seleccionado
    selected_role = ""

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

    # AnimatedSwitcher para animar la aparición del formulario con efecto de fundido
    login_form_switcher = ft.AnimatedSwitcher(
        duration=300,
        transition=ft.AnimatedSwitcherTransition.FADE,
        content=ft.Container(key="empty")  # Estado inicial: contenedor vacío
    )

    # Función para manejar el clic en un rol
    def on_role_click(e, role):
        nonlocal selected_role
        selected_role = role
        # Se actualiza el content del AnimatedSwitcher con el formulario actualizado
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

    # Creación de los botones para cada rol usando la paleta
    btn_admin = vertical_button(ft.icons.ADMIN_PANEL_SETTINGS, "ADMINISTRADOR", "admin", COLOR_DARK_PURPLE)
    btn_coach = vertical_button(ft.icons.SPORTS_TENNIS, "ENTRENADOR", "coach", COLOR_MUTED_PINK)
    btn_user = vertical_button(ft.icons.PERSON, "USUARIO", "user", COLOR_SOFT_GREEN)

    # Organización de los botones en una fila horizontal
    roles_row = ft.Row(
        controls=[btn_admin, btn_coach, btn_user],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Contenido interno del contenedor: el formulario (arriba) y los botones (abajo)
    container_content = ft.Column(
        controls=[
            login_form_switcher,
            ft.Divider(height=20, color=COLOR_DARK_PURPLE),
            roles_row
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Contenedor "card" estilizado con fondo, borde redondeado y sombra
    container = ft.Container(
        content=container_content,
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
