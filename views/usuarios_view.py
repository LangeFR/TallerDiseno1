# tallerdiseno1/views/usuarios_view.py
import flet as ft

def create_usuarios_view(controller, page, content):
    """
    Crea la vista de usuarios y retorna la vista inicial junto con la función para mostrar
    los usuarios filtrados y sus detalles.

    Parámetros:
        controller: El controlador que proporciona filtrar_usuarios.
        page (ft.Page): La página principal para actualizar la interfaz.
        content (ft.Column): Contenedor donde se mostrará la vista de usuarios.

    Retorna:
        tuple: (usuarios_view, mostrar_usuarios_view)
    """

    def mostrar_info_usuario(usuario):
        usuario_info = ft.Column(
            [
                ft.Text("Información del Usuario", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                ft.Text(f"Nombre: {usuario.nombre}"),
                ft.Text(f"Edad: {usuario.edad}"),
                ft.Text(f"Identificación: {usuario.num_identificacion}"),
                ft.Text(f"Correo: {usuario.correo}"),
                ft.Text(f"Teléfono: {usuario.telefono}"),
                ft.Text(f"Estado: {usuario.estado}"),
                ft.ElevatedButton(
                    "Regresar",
                    on_click=lambda e: mostrar_usuarios_view("inscrito")
                ),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
        )
        content.controls.clear()
        content.controls.append(usuario_info)
        page.update()

    def mostrar_usuarios_view(estado):
        usuarios_filtrados = controller.filtrar_usuarios(estado)
        usuarios_list = [
            ft.ListTile(
                title=ft.Text(f"{usuario.nombre} {usuario.apellidos}", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(f"Estado: {usuario.estado}"),
                leading=ft.Icon(ft.icons.PERSON),
                on_click=lambda e, u=usuario: mostrar_info_usuario(u)
            )
            for usuario in usuarios_filtrados
        ]
        vista_usuarios = ft.ListView(
            [
                ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=10, thickness=2),
                *usuarios_list,
            ],
            spacing=10,
            expand=True,
        )
        content.controls.clear()
        content.controls.append(vista_usuarios)
        page.update()

    # Vista inicial: muestra dos botones para filtrar por inscritos o matriculados.
    usuarios_view = ft.Column(
        [
            ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, thickness=2),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Usuarios Inscritos",
                        on_click=lambda e: mostrar_usuarios_view("inscrito")
                    ),
                    ft.ElevatedButton(
                        "Usuarios Matriculados",
                        on_click=lambda e: mostrar_usuarios_view("matriculado")
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            )
        ],
        spacing=10
    )
    return usuarios_view, mostrar_usuarios_view


