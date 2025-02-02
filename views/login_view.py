import flet as ft

def main(page: ft.Page):
    # Configurar título y alineación de la página para centrar el contenedor
    page.title = "Inicio de Sesión - Roles"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = ft.colors.SURFACE_VARIANT  # Opcional: color de fondo

    # Función para manejar el clic en los botones
    def on_button_click(e, role):
        print(f"Iniciado sesión como: {role}")

    # Crear botones para Admin, Coach y User
    btn_admin = ft.ElevatedButton(
        text="ADMINISTRADOR",
        on_click=lambda e: on_button_click(e, "admin"),
        icon=ft.icons.ADMIN_PANEL_SETTINGS,
        bgcolor=ft.colors.BLUE,
        width=200
    )

    btn_coach = ft.ElevatedButton(
        text="ENTRENADOR",
        on_click=lambda e: on_button_click(e, "coach"),
        icon=ft.icons.SPORTS_TENNIS,
        bgcolor=ft.colors.GREEN,
        width=200
    )

    btn_user = ft.ElevatedButton(
        text="USUARIO",
        on_click=lambda e: on_button_click(e, "user"),
        icon=ft.icons.PERSON,
        bgcolor=ft.colors.RED,
        width=200
    )

    # Columna para alinear verticalmente los botones
    buttons_column = ft.Column(
        controls=[btn_admin, btn_coach, btn_user],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Contenedor centrado que agrupa la columna de botones
    container = ft.Container(
        content=buttons_column,
        width=300,
        height=300,
        padding=20,
        alignment=ft.alignment.center,  # Centra el contenido dentro del contenedor
        border_radius=ft.border_radius.all(10),  # Usar la función del módulo
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
