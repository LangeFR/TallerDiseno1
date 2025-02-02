import flet as ft

def main(page: ft.Page):
    # Configuración de la página para centrar el contenedor
    page.title = "Inicio de Sesión - Roles"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.SURFACE_VARIANT

    # Variables y controles para el formulario de login (inicialmente oculto)
    selected_role = None
    username_field = ft.TextField(label="Usuario", width=300)
    password_field = ft.TextField(label="Contraseña", password=True, width=300)
    login_button = ft.ElevatedButton(text="Ingresar", width=300)
    role_text = ft.Text(value="", size=18, weight=ft.FontWeight.W_600)

    login_form = ft.Column(
        controls=[
            role_text,
            username_field,
            password_field,
            login_button
        ],
        visible=False,
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Función que se invoca al seleccionar un rol
    def on_role_click(e, role):
        nonlocal selected_role
        selected_role = role
        role_text.value = f"Iniciar sesión como: {role.upper()}"
        login_form.visible = True
        page.update()

    # Función auxiliar para crear un botón con icono y texto en disposición vertical
    def vertical_button(icon, label, role, bgcolor):
        return ft.ElevatedButton(
            # Se define el contenido del botón con un Column
            content=ft.Column(
                controls=[
                    ft.Icon(icon, size=40),
                    ft.Text(label, size=14)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5
            ),
            on_click=lambda e: on_role_click(e, role),
            bgcolor=bgcolor,
            width=150
        )

    # Creación de los botones para cada rol con el texto debajo del icono
    btn_admin = vertical_button(ft.icons.ADMIN_PANEL_SETTINGS, "ADMINISTRADOR", "admin", ft.colors.BLUE)
    btn_coach = vertical_button(ft.icons.SPORTS_TENNIS, "ENTRENADOR", "coach", ft.colors.GREEN)
    btn_user = vertical_button(ft.icons.PERSON, "USUARIO", "user", ft.colors.RED)

    # Organizar los botones en una fila horizontal
    roles_row = ft.Row(
        controls=[btn_admin, btn_coach, btn_user],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Contenido interno del contenedor: el formulario en la parte superior y debajo la fila de botones
    container_content = ft.Column(
        controls=[
            login_form,
            ft.Divider(height=20),
            roles_row
        ],
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Definición del contenedor con fondo, borde y sombra para que se vea
    container = ft.Container(
        content=container_content,
        width=600,
        padding=20,
        alignment=ft.alignment.center,
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.colors.WHITE,
        border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
        shadow=ft.BoxShadow(
            color=ft.colors.BLACK38,
            blur_radius=10,
            spread_radius=1,
            offset=ft.Offset(2, 2)
        )
    )

    # Agregar el contenedor a la página
    page.add(container)

if __name__ == "__main__":
    ft.app(target=main)
